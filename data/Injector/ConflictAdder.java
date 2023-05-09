import java.io.*;
import java.sql.*;
import java.util.*;
import java.text.NumberFormat;
import org.semanticweb.kaon2.api.*;
import org.semanticweb.kaon2.api.logic.*;
import org.semanticweb.kaon2.api.reasoner.*;
import org.semanticweb.kaon2.api.owl.elements.*;

public class ConflictAdder {

    /** The URI prefix of extra individuals */
    final static String URI_PREFIX = "ex:";

    /** Database dbConnection */
    private Connection dbConnection;

    /** Namespaces */
    private Namespaces namespaces;

    /** SQL prepared statements */
    private PreparedStatement pinsIndStmt;
    private PreparedStatement pinsDiffStmt;
    private HashMap<String,PreparedStatement> pinsClassStmts;
    private HashMap<String,PreparedStatement> pinsRoleStmts;

    /** Mapping from individual URI to DB id */
    private HashMap<String,Integer> nodeIds;

    /** Mapping from datatype URI to literal id */
    private HashMap<String,Integer> typeIds;

    /** The number of individuals */
    private int numIndividuals;
    private int numExtIndividuals;

    /** The number of assertions */
    private int numAssertions;
    private int numOrgAssertions;

    /** The list of functional and inverse functional properties */
    private ArrayList<String> funcProperties;

    /** The list of classes that have disjoint classes */
    private ArrayList<String> confClasses;
    private ArrayList<ArrayList<String>> confDisjoints;

    /** Ontology dbConnection */
    private KAON2Connection onConnection;

    /**
     * Creates a new dbConnection if there is none yet 
     * @throws KAON2Exception
     */
    public void makeConnection() throws KAON2Exception {
        if (onConnection == null) {
            onConnection = KAON2Manager.newConnection();
            DefaultOntologyResolver resolver = new DefaultOntologyResolver();
            resolver.registerReplacement(
                "http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl",
                "file:univ-bench.owl");
            resolver.registerReplacement(
                "http://uob.iodt.ibm.com/univ-bench-lite.owl",
                "file:univ-bench-lite.owl");
            resolver.registerReplacement(
                "http://172.16.83.69/univ-bench-lite.owl",
                "file:univ-bench-lite.owl");
            resolver.registerReplacement(
                "http://uob.iodt.ibm.com/univ-bench-dl.owl",
                "file:univ-bench-dl-.owl");
            resolver.registerReplacement(
                "http://semantics.crl.ibm.com/univ-bench-dl.owl",
                "file:univ-bench-dlnn.owl");
            resolver.registerReplacement(
                "http://www.biopax.org/release/biopax-level1.owl",
                "file:biopax-level1.owl");
            resolver.registerReplacement(
                "http://www.biopax.org/release/biopax-level2.owl",
                "file:biopax-level2.owl");
            onConnection.setOntologyResolver(resolver);
        }
    }

    /**
     * closes an existing KAON2Connection and stores datatypes
     * @throws Exception
     */
    public void endRunning() throws Exception {
        if (onConnection != null)
            onConnection.close(); // GANZ HEFTIGES TODO memory leak?
        onConnection = null;
    }

    /**
     * loads an ontology. If there is no open dbConnection, a new one is created
     * @param name Name of the ontology to be loaded. Either starts with http,
     * https or ftp, or it will be loaded from a local file with the given name
     * @return The loaded ontology
     * @throws KAON2Exception
     * @throws InterruptedException
     */
    public Ontology loadOntology(String name)
    throws KAON2Exception, InterruptedException {
        makeConnection();

        OntologyResolver resolver = onConnection.getOntologyResolver();
        if (resolver instanceof DefaultOntologyResolver) {
            DefaultOntologyResolver res = (DefaultOntologyResolver)resolver;
            if (!name.startsWith("http:"))
                if (!name.startsWith("https:"))
                    if (!name.startsWith("ftp:"))
                        if (!name.startsWith("file:"))
                            res.registerReplacement(name, "file:" + name);
            resolver = res;
        }
        onConnection.setOntologyResolver(resolver);

        return onConnection.openOntology(name, new HashMap<String,Object>());
    }

    /** Converts a name */
    private void convert(StringBuffer namebuf) {
        for (int i = 0; i < namebuf.length(); i++)
        if (namebuf.charAt(i) == ':' || namebuf.charAt(i) == '-' ||
            namebuf.charAt(i) == '.')
            namebuf.setCharAt(i, '_');
        if (namebuf.length() > 63)
            namebuf.setLength(63);
    }

    /** Creates a new instance of DBDumper */
    public ConflictAdder(String driver, String url, String user, String pwd)
    throws Exception {
        Class.forName(driver);
        dbConnection = DriverManager.getConnection(url, user, pwd);
        dbConnection.setTransactionIsolation(
            dbConnection.TRANSACTION_READ_COMMITTED);
    }


    /** Prepares the SQL statements and initializes related tables */
    public void prepareTables(Ontology ontology) throws Exception {
        namespaces = new Namespaces();
        namespaces.registerStandardPrefixes();

        Statement stmt = dbConnection.createStatement();

        String cfields = "(id int not null, " +
                         "node int not null, " +
                         "expanded tinyint null, " +
                         "is_new tinyint null, " +
                         "primary key (id), " +
                         "unique (node), " +
                         "index (expanded), " +
                         "index (is_new))";
        String rfields = "(id int not null, " +
                         "fnode int not null, " +
                         "tnode int not null, " +
                         "is_new tinyint null, " +
                         "primary key (id), " +
                         "unique (fnode,tnode), " +
                         "unique (tnode,fnode), " +
                         "index (is_new))";

        numIndividuals = 0;
        numExtIndividuals = 0;
        ResultSet rs = stmt.executeQuery("select max(id) from individual");
        if (rs.next())
            numIndividuals = rs.getInt(1);
        rs.close();

        ArrayList tables = new ArrayList();
        rs = stmt.executeQuery("show tables like '%\\_%'");
        while (rs.next())
        if (rs.getString(1).charAt(0) != '_')
            tables.add(rs.getString(1));
        rs.close();

        numAssertions = 0;
        for (int i = 0; i < tables.size(); i++) {
            rs = stmt.executeQuery("select max(id) from " + tables.get(i) +
                                   " where is_new=0");
            if (rs.next() && numAssertions < rs.getInt(1))
                numAssertions = rs.getInt(1);
            rs.close();
        }
        numOrgAssertions = numAssertions;

        pinsIndStmt = dbConnection.prepareStatement(
            "insert into individual values(?,?,0)");
        pinsDiffStmt = dbConnection.prepareStatement(
            "insert into owl_diffFrom values(?,?,?,0)");

        pinsClassStmts = new HashMap<String,PreparedStatement>();
        pinsRoleStmts = new HashMap<String,PreparedStatement>();
        confClasses = new ArrayList<String>();
        confDisjoints = new ArrayList<ArrayList<String>>();
        funcProperties = new ArrayList<String>();
        ArrayList<OWLClass> clist = new ArrayList<OWLClass>();
        PreparedStatement pinsClassStmt, pinsRoleStmt;

        Set<OWLClass> classes =
            ontology.createEntityRequest(OWLClass.class).getAll();
        for (OWLClass c: classes)
        if (!c.equals(KAON2Manager.factory().thing()) &&
            !pinsClassStmts.containsKey(c.getURI())) {
            namespaces.ensureNamespacePrefixExists(c.getURI());
            StringBuffer namebuf = new StringBuffer();
            c.toString(namebuf, namespaces);
            convert(namebuf);
            stmt.execute("create table if not exists " + namebuf.toString() +
                         cfields);
            pinsClassStmt = dbConnection.prepareStatement(
                "insert into " + namebuf.toString() + " values(?,?,0,0)");
            pinsClassStmts.put(c.getURI(), pinsClassStmt);
            clist.add(c);
        }
        if (!dbConnection.getAutoCommit()) dbConnection.commit();

        Set<ObjectProperty> oproperties =
            ontology.createEntityRequest(ObjectProperty.class).getAll();
        for (ObjectProperty op: oproperties)
        if (!pinsRoleStmts.containsKey(op.getURI())) {
            namespaces.ensureNamespacePrefixExists(op.getURI());
            StringBuffer namebuf = new StringBuffer();
            op.toString(namebuf, namespaces);
            convert(namebuf);
            stmt.execute("create table if not exists " + namebuf.toString() +
                         rfields);
            pinsRoleStmt = dbConnection.prepareStatement(
                "insert into " + namebuf.toString() + " values(?,?,?,0)");
            pinsRoleStmts.put(op.getURI(), pinsRoleStmt);
            if (op.isFunctional(ontology) || op.isInverseFunctional(ontology))
                funcProperties.add(op.getURI());
        }
        if (!dbConnection.getAutoCommit()) dbConnection.commit();

        Set<DataProperty> dproperties =
            ontology.createEntityRequest(DataProperty.class).getAll();
        for (DataProperty dp: dproperties)
            namespaces.ensureNamespacePrefixExists(dp.getURI());

        Set<Individual> individuals =
            ontology.createEntityRequest(Individual.class).getAll();
        for (Individual ind: individuals)
            namespaces.ensureNamespacePrefixExists(ind.getURI());

        stmt.close();

        Reasoner reasoner = ontology.createReasoner();
        for (int i = 0; i < clist.size(); i++) {
            ArrayList<String> disjoints = new ArrayList<String>();
            for (int j = 0; j < clist.size(); j++)
            if (j != i && reasoner.subsumedBy(
                clist.get(i), KAON2Manager.factory().objectNot(clist.get(j))))
                disjoints.add(clist.get(j).getURI());
            if (disjoints.size() > 0) {
                confClasses.add(clist.get(i).getURI());
                confDisjoints.add(disjoints);
            }
        }
        reasoner.dispose();
    }

    /** Gets the name of a term */
    private String getName(Term term) {
        StringBuffer namebuf = new StringBuffer();
        term.toString(namebuf, namespaces);
        return namebuf.toString();
    }

    /** Creates a given number of conflicts,
     *  returns the number of added assertions */
    private int createAssertions(Reasoner reasoner, int count) 
    throws Exception {
        int nadded = 0, ncur = 0;
        double rand;
        ObjectProperty op;
        OWLClass cls;
        Term[] terms;
        String name;
        int subjid, objid, cmpid;
        ArrayList<String> disjoints;
        PreparedStatement pselIndex = dbConnection.prepareStatement(
            "select id from individual where name=?");
        PreparedStatement pinsRoleStmt, pinsClassStmt;
        ResultSet rs;

        while (ncur < count) {
            rand = Math.random() * (funcProperties.size()+confClasses.size());
            cmpid = (int)rand;
            if (cmpid < funcProperties.size()) {
                op = KAON2Manager.factory().objectProperty(
                    funcProperties.get(cmpid));
                pinsRoleStmt=(PreparedStatement)pinsRoleStmts.get(op.getURI());
                if (pinsRoleStmt == null) {
                    System.out.println("Error: property " + op.getURI() +
                                       " has no insertion statement");
                    continue;
                }

                subjid = objid = 0;
                Query q = reasoner.createQuery(op);
                q.open();
                rand = Math.random() * q.getNumberOfTuples();
                while (!q.afterLast() && rand >= 0) {
                    terms = q.tupleBuffer();
                    name = getName(terms[0]);
                    pselIndex.setString(1, name);
                    rs = pselIndex.executeQuery();
                    if (rs.next())
                        subjid = rs.getInt(1);
                    else
                        System.out.println("Error: individual " + name +
                                           " is not found in the database");
                    rs.close();
                    name = getName(terms[1]);
                    pselIndex.setString(1, name);
                    rs = pselIndex.executeQuery();
                    if (rs.next())
                        subjid = rs.getInt(1);
                    else
                        System.out.println("Error: individual " + name +
                                           " is not found in the database");
                    rs.close();
                    q.next();
                    rand--;
                }
                q.close();
                q.dispose();

                if (subjid == 0) {
                    numExtIndividuals++;
                    pinsIndStmt.setInt(1, numIndividuals+numExtIndividuals);
                    pinsIndStmt.setString(2, URI_PREFIX+numExtIndividuals);
                    pinsIndStmt.executeUpdate();
                    subjid = numIndividuals + numExtIndividuals;
                }
                if (objid == 0) {
                    numExtIndividuals++;
                    pinsIndStmt.setInt(1, numIndividuals+numExtIndividuals);
                    pinsIndStmt.setString(2, URI_PREFIX+numExtIndividuals);
                    pinsIndStmt.executeUpdate();
                    objid = numIndividuals + numExtIndividuals;
                    pinsRoleStmt.setInt(1, ++numAssertions);
                    pinsRoleStmt.setInt(2, subjid);
                    pinsRoleStmt.setInt(3, objid);
                    try {
                        pinsRoleStmt.executeUpdate();
                        nadded++;
                    }
                    catch (SQLException e) {
                        System.out.println();
                        System.out.println(e);
                        --numAssertions;
                    }
                }

                numExtIndividuals++;
                pinsIndStmt.setInt(1, numIndividuals+numExtIndividuals);
                pinsIndStmt.setString(2, URI_PREFIX+numExtIndividuals);
                pinsIndStmt.executeUpdate();
                cmpid = numIndividuals + numExtIndividuals;
                pinsRoleStmt.setInt(1, ++numAssertions);
                if (op.isInverseFunctional(reasoner.getOntology())) {
                    pinsRoleStmt.setInt(2, cmpid);
                    pinsRoleStmt.setInt(3, objid);
                    try {
                        pinsRoleStmt.executeUpdate();
                        nadded++;
                    }
                    catch (SQLException e) {
                        System.out.println();
                        System.out.println(e);
                        --numAssertions;
                    }
                    pinsDiffStmt.setInt(1, ++numAssertions);
                    if (subjid < cmpid) {
                        pinsDiffStmt.setInt(2, subjid);
                        pinsDiffStmt.setInt(3, cmpid);
                    }
                    else {
                        pinsDiffStmt.setInt(2, cmpid);
                        pinsDiffStmt.setInt(3, subjid);
                    }
                    try {
                        pinsDiffStmt.executeUpdate();
                        nadded++;
                    }
                    catch (SQLException e) {
                        System.out.println();
                        System.out.println(e);
                        --numAssertions;
                    }
                }
                else {
                    pinsRoleStmt.setInt(2, subjid);
                    pinsRoleStmt.setInt(3, cmpid);
                    try {
                        pinsRoleStmt.executeUpdate();
                        nadded++;
                    }
                    catch (SQLException e) {
                        System.out.println();
                        System.out.println(e);
                        --numAssertions;
                    }
                    pinsDiffStmt.setInt(1, ++numAssertions);
                    if (objid < cmpid) {
                        pinsDiffStmt.setInt(2, objid);
                        pinsDiffStmt.setInt(3, cmpid);
                    }
                    else {
                        pinsDiffStmt.setInt(2, cmpid);
                        pinsDiffStmt.setInt(3, objid);
                    }
                    try {
                        pinsDiffStmt.executeUpdate();
                        nadded++;
                    }
                    catch (SQLException e) {
                        System.out.println();
                        System.out.println(e);
                        --numAssertions;
                    }
                }
            }

            else {
                cmpid -= funcProperties.size();
                cls = KAON2Manager.factory().owlClass(confClasses.get(cmpid));

                subjid = 0;
                Query q = reasoner.createQuery(cls);
                q.open();
                rand = Math.random() * q.getNumberOfTuples();
                while (!q.afterLast() && rand >= 0) {
                    terms = q.tupleBuffer();
                    name = getName(terms[0]);
                    pselIndex.setString(1, name);
                    rs = pselIndex.executeQuery();
                    if (rs.next())
                        subjid = rs.getInt(1);
                    else
                        System.out.println("Error: individual " + name +
                                           " is not found in the database");
                    rs.close();
                    q.next();
                    rand--;
                }
                q.close();
                q.dispose();

                if (subjid == 0) {
                    numExtIndividuals++;
                    pinsIndStmt.setInt(1, numIndividuals+numExtIndividuals);
                    pinsIndStmt.setString(2, URI_PREFIX+numExtIndividuals);
                    pinsIndStmt.executeUpdate();
                    subjid = numIndividuals + numExtIndividuals;
                    pinsClassStmt =
                        (PreparedStatement)pinsClassStmts.get(cls.getURI());
                    if (pinsClassStmt == null) {
                        System.out.println("Error: class " + cls.getURI() +
                                           " has no insertion statement");
                        continue;
                    }
                    else {
                        pinsClassStmt.setInt(1, ++numAssertions);
                        pinsClassStmt.setInt(2, subjid);
                        try {
                            pinsClassStmt.executeUpdate();
                            nadded++;
                        }
                        catch (SQLException e) {
                            System.out.println();
                            System.out.println(e);
                            --numAssertions;
                        }
                    }
                }

                disjoints = confDisjoints.get(cmpid);
                rand = Math.random() * disjoints.size();
                name = disjoints.get((int)rand);
                pinsClassStmt =
                    (PreparedStatement)pinsClassStmts.get(name);
                if (pinsClassStmt == null) {
                    System.out.println("Error: class " + name +
                                       " has no insertion statement");
                    continue;
                }
                else {
                    pinsClassStmt.setInt(1, ++numAssertions);
                    pinsClassStmt.setInt(2, subjid);
                    try {
                        pinsClassStmt.executeUpdate();
                        nadded++;
                    }
                    catch (SQLException e) {
                        System.out.println();
                        System.out.println(e);
                        --numAssertions;
                        continue;
                    }
                }
            }
            ncur++;
        }

        if (!dbConnection.getAutoCommit()) dbConnection.commit();
        return nadded;
    }

    /**
     * Adds the conflicts
     *
     * @param url   the URL of the given ontology
     * @param count the number of assertions that introduce conflicts
     * @param init  whether it is needed to prepare all tables
     */
    public void addConflicts(String url, int count, boolean init)
    throws Exception {
        if (count <= 0) return;

        if (init)
            System.out.println("Initializing predicate tables...");
        else
            System.out.printf("Adding %d conflicts to %s...", count, url);

        Ontology ontology = loadOntology(url);

        if (init) {
            prepareTables(ontology);
            System.out.println("#C-Classes = " + confClasses.size() +
                               ", #C-Properties = " + funcProperties.size() +
                               ", #Individuals = " + numIndividuals +
                               ", #Assertions = " + numAssertions);
            if (numIndividuals == 0 ||
                (confClasses.size() == 0 && funcProperties.size() == 0))
                return;
            System.out.printf("Adding %d conflicts to %s...", count, url);
        }

        Reasoner reasoner = ontology.createReasoner();
/*
        ArrayList<Predicate> preds = new ArrayList<Predicate>();
        for (String cstr: confClasses)
            preds.add(KAON2Manager.factory().owlClass(cstr));
        for (String fstr: funcProperties)
            preds.add(KAON2Manager.factory().objectProperty(fstr));
        reasoner.materializeExtensions(preds, true);
        System.out.print("...");
*/
        int num = createAssertions(reasoner, count);
        System.out.printf("%d assertions added%n", num);

        reasoner.dispose();

        onConnection.closeOntologies(onConnection.getOntologies());
    }


    public static void main(String[] args) throws Exception {
        // TODO code application logic here
        if (args.length < 3) {
            System.out.println("Usage java ConflictAdder " +
                "<db name> <#conflicts> <url> ... <url>");
            System.exit(1);
        }

        long st_time = System.currentTimeMillis();
        int num_confs = Integer.parseInt(args[1]);
        Properties props = new Properties();
        props.load(new FileInputStream("mysql.ini"));
        String host = props.getProperty("host", "localhost");
        String dbUser = props.getProperty("user");
        String dbPass = props.getProperty("password");
        ConflictAdder adder = new ConflictAdder(
            "com.mysql.jdbc.Driver", "jdbc:mysql://" + host + "/" + args[0],
            dbUser, dbPass);

        for (int i = 2; i < args.length & num_confs > 0; i++) {
            int to_add = num_confs/(args.length-i);
            if (to_add <= 0) to_add = 1;
            adder.addConflicts(args[i], to_add, i == 2);
            num_confs -= to_add;
        }
        adder.endRunning();

        long ed_time = System.currentTimeMillis();
        NumberFormat nf = NumberFormat.getIntegerInstance();
        nf.setGroupingUsed(true);
        long total_mem = Runtime.getRuntime().totalMemory();
        long free_mem = Runtime.getRuntime().freeMemory();
        System.out.println("Used " +  nf.format(ed_time-st_time) +
            " milliseconds and " + nf.format(total_mem-free_mem) +
            " bytes (JVM " + nf.format(total_mem) + " bytes)");
    }

}
