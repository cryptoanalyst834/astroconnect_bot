const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  telegramId: { type: String, required: true, unique: true },
  username: { type: String },
  fullName: { type: String },
  birthDate: { type: Date },
  gender: { type: String, enum: ['male', 'female', 'other'] },
  bio: { type: String, maxlength: 500 },
  photoUrl: { type: String },
  audioIntroUrl: { type: String }, // ссылка на аудио-приветствие
  location: {
    type: { type: String, enum: ['Point'], default: 'Point' },
    coordinates: { type: [Number] }, // [longitude, latitude]
  },
  interests: [String],
  giftsReceived: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Gift' }],
  createdAt: { type: Date, default: Date.now },
}, { timestamps: true });

userSchema.index({ location: '2dsphere' });

module.exports = mongoose.model('User', userSchema);

