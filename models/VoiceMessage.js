const mongoose = require("mongoose");

const VoiceMessageSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  audioUrl: {
    type: String,
    required: true,
  },
  duration: {
    type: Number, // в секундах
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("VoiceMessage", VoiceMessageSchema);
