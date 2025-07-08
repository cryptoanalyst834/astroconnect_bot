const express = require('express');
const router = express.Router();
const multer = require('multer');
const audioController = require('../controllers/audio.controller');

const storage = multer.memoryStorage();
const upload = multer({ storage });

router.post('/upload', upload.single('audio'), audioController.uploadAudio);
router.get('/:id', audioController.getAudio);

module.exports = router;
