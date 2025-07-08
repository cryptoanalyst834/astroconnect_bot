const mongoose = require("mongoose");

const UsageLimitSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
    unique: true,
  },
  dailySwipeLimit: {
    type: Number,
    default: 50,
  },
  swipesUsedToday: {
    type: Number,
    default: 0,
  },
  lastReset: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("UsageLimit", UsageLimitSchema);
