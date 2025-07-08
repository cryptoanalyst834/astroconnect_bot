const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const auth = require('../middlewares/auth');
const upload = require('../middlewares/upload');

router.get('/profile', auth, userController.getProfile);
router.put('/profile', auth, userController.updateProfile);
router.post('/audio', auth, upload.single('audio'), userController.uploadAudio);

module.exports = router;
