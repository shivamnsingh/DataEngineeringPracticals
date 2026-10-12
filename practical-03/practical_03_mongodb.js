// Practical 3: MongoDB Operations
// Aim: To perform single and multiple document insertion and retrieval
//      using the MongoDB shell (mongosh).
//
// How to run:   mongosh
//               > use practical3
//               > load("practical_03_mongodb.js")

// >>> CHANGE THIS TO YOUR NAME <<<
const STUDENT_NAME = "Shivam Singh";

// Start clean so re-running does not create duplicate documents
db.items.drop();
db.products.drop();

// ---------------------------------------------------------------
print("\n## Step 1: Insert Single Document");
print("Query: db.items.insertOne({ name: \"laptop\", price: 999 });");
printjson(db.items.insertOne({ name: "laptop", price: 999 }));

// ---------------------------------------------------------------
print("\n## Step 2: View Inserted Document");
print("Query: db.items.find();");
printjson(db.items.find().toArray());

// ---------------------------------------------------------------
print("\n## Step 3: Insert Multiple Documents");
print("Query: db.products.insertMany([...3 products...]);");
printjson(db.products.insertMany([
  { name: "phone", price: 500, stock: 10 },
  { name: "tablet", price: 300, stock: 5 },
  { name: "watch", price: 150, stock: 0 }
]));

// ---------------------------------------------------------------
print("\n## Step 4: View Products in Formatted JSON");
print("Query: db.products.find().pretty();");
printjson(db.products.find().toArray());

// ---------------------------------------------------------------
print("\n========================================");
print("Submitted by: " + STUDENT_NAME);
print("========================================");