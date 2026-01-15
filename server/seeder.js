const mongoose = require('mongoose');
const dotenv = require('dotenv');
const bcrypt = require('bcryptjs');
const books = require('./data/books.js');
const Book = require('./models/Book.js');
const User = require('./models/User.js');

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

const seedDemoUser = async () => {
  const email = 'demo123@gmail.com';

  const existingUser = await User.findOne({ email });
  if (existingUser) {
    console.log('Demo user already exists');
    return;
  }

  const hashedPassword = await bcrypt.hash('demo123', 10);

  await User.create({
    name: 'Demo User',
    email,
    password: hashedPassword,
  });

  console.log('Demo user created');
};

const importData = async () => {
  try {
    await Book.deleteMany();
    await Book.insertMany(books);

    // 🔥 ADD THIS LINE
    await seedDemoUser();

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
    await User.deleteMany();

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
};

runSeeder();
