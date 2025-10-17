const mongoose = require('mongoose');
const dotenv = require('dotenv');
const books = require('./data/books.js');
const Book = require('./models/Book.js');
const User = require('./models/User.js'); // Import other models if you need to seed them

dotenv.config();

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('MongoDB Connected for Seeding...');
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
};

const importData = async () => {
  try {
    // Clear existing data before importing
    await Book.deleteMany();
    
    await Book.insertMany(books);

    console.log('Data Imported Successfully!');
    process.exit();
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

const destroyData = async () => {
  try {
    await Book.deleteMany();
    await User.deleteMany(); // Example: clear users too
    // await Cart.deleteMany();

    console.log('Data Destroyed Successfully!');
    process.exit();
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

const runSeeder = async () => {
    await connectDB();

    if (process.argv[2] === '-d') {
        await destroyData();
    } else {
        await importData();
    }
}

runSeeder();