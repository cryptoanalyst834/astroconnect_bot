const User = require('../models/User');
const UsageLimit = require('../models/UsageLimit');

exports.getProfile = async (req, res) => {
  const user = await User.findById(req.userId);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
};

exports.updateProfile = async (req, res) => {
  const update = req.body;
  const user = await User.findByIdAndUpdate(req.userId, update, { new: true });
  res.json(user);
};

exports.uploadAudio = async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });
  const user = await User.findById(req.userId);
  user.audio = req.file.path;
  await user.save();
  res.json({ message: 'Audio uploaded successfully', audioUrl: user.audio });
};
