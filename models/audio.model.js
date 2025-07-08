const mongoose = require('mongoose');

const AudioSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  filename: { type: String, required: true },
  uploadDate: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Audio', AudioSchema);
