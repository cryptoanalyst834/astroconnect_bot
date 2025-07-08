const express = require("express");
const router = express.Router();
const giftController = require("../controllers/giftController");

router.post("/send", giftController.sendGift);
router.get("/received/:userId", giftController.getReceivedGifts);

module.exports = router;
