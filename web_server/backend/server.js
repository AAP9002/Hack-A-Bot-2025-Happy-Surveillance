require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const app = express();
const port = 3000;

// Configure database

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch((err) => console.error('Error connecting to MongoDB:', err));


// Define Mongoose Schema
const emotionRecordSchema = new mongoose.Schema({
    image: String,  // Base64-encoded image
    emotion: String,
    image_type: String,
    date_added: Date
});

// Create Model
const EmotionRecord = mongoose.model("emotion_records", emotionRecordSchema);


// Middleware enables
app.use(express.json());
app.use(cors());

// Basic route
app.get('/', (req, res) => {
  res.send('Hello World!');
});


// GETTERS
app.get("/images/:emotion", async (req, res) => {
    console.log("received")
    try {
        // const emotion = req.params.emotion; // Get emotion from URL
        const happyImages = await EmotionRecord.find({ emotion: "happy" }).sort({ date_added: -1 });
        console.log(happyImages)
        // Send image data along with metadata
        res.json(happyImages);
    } catch (error) {
        console.error("Error fetching images:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});





// POST route
// app.post('/addHappyPerson', (req, res) => {
//     const { image } = req.body;
//     res.json({ message: `Received ${name} who is ${age} years old.` });
// });

// app.post('/addSadPerson', (req, res) => {
//     const { image } = req.body;
//     res.json({ message: `Received ${name} who is ${age} years old.` });
// });


// app.post('/addHappyPerson', upload.single('image'), async (req, res) => {
//     try {
//         // Convert image buffer to base64
//         const imageBase64 = req.file.buffer.toString('base64');

//         // Save the image to the database
//         const newImage = new Image({
//             emotion: "happy",
//             image: imageBase64,
//             contentType: "png",
//         });

//         await newImage.save();
//         res.status(200).json({ message: 'Image uploaded successfully!' });
//     } catch (error) {
//         res.status(500).json({ message: 'Error uploading image', error });
//     }
// });



// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});