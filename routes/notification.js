const express = require("express");
const router = express.Router();
const notificationController = require("../controllers/notificationController");

router.post("/send", notificationController.sendNotification);
router.get("/user/:userId", notificationController.getNotifications);

module.exports = router;
