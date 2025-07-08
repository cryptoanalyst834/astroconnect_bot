const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController");
const multer = require("multer");

// Настройка multer
const storage = multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + "-" + file.originalname;
    cb(null, uniqueName);
  },
});
const upload = multer({ storage });

// Роуты
router.get("/:id", userController.getProfile);
router.put("/:id", userController.updateProfile);
router.post("/upload-audio", upload.single("audio"), userController.uploadAudio);

module.exports = router;
