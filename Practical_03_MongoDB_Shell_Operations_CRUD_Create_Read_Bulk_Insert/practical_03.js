/*
Practical 3: MongoDB Shell Operations (CRUD - Create, Read, Bulk Insert)
Name: Shivam Singh | Roll No. 56 | Student ID 5135873 | T.Y. Data Science
*/

// ===== Task 1: Single Document Insertion & Data Querying =====
// 1. Insert a single document into items collection
db.items.insertOne({ name: "laptop", price: 999 });

// 2. View the document just added
db.items.find();


// ===== Task 2: Bulk Document Insertion & Pretty Printing =====
// Insert multiple product documents
db.products.insertMany([
  { name: "phone", price: 500, stock: 10 },
  { name: "tablet", price: 300, stock: 5 },
  { name: "watch", price: 150, stock: 0 }
]);

// Formatted Query
db.products.find().pretty();

