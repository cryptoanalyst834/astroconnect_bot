const mongoose = require('mongoose');
const { GridFSBucket } = require('mongodb');
const Audio = require('../models/audio.model');
const { Readable } = require('stream');

let gfs;

mongoose.connection.once('open', () => {
  gfs = new GridFSBucket(mongoose.connection.db, {
    bucketName: 'audios'
  });
});

exports.uploadAudio = async (req, res) => {
  try {
    const { userId } = req.body;
    const file = req.file;

    const readableStream = Readable.from(file.buffer);
    const uploadStream = gfs.openUploadStream(file.originalname, {
      contentType: file.mimetype,
    });

    readableStream.pipe(uploadStream)
      .on('error', () => res.status(500).send('Upload error'))
      .on('finish', async () => {
        const audio = new Audio({ userId, filename: file.originalname });
        await audio.save();
        res.status(201).json({ message: 'Uploaded', fileId: uploadStream.id });
      });
  } catch (err) {
    res.status(500).send(err.message);
  }
};

exports.getAudio = async (req, res) => {
  try {
    const fileId = new mongoose.Types.ObjectId(req.params.id);
    gfs.openDownloadStream(fileId).pipe(res);
  } catch {
    res.status(404).send('Not found');
  }
};
