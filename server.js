import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import cors from 'cors';
import morgan from 'morgan';
import authRoutes from './routes/auth.js';
import profileRoutes from './routes/profiles.js';
import giftRoutes from './routes/gifts.js';
import filterRoutes from './routes/filters.js';
import notificationRoutes from './routes/notifications.js';
import audioRoutes from './routes/audio.js';

dotenv.config();

const app = express();

app.use(cors());
app.use(morgan('dev'));
app.use(express.json({ limit: '50mb' }));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/profiles', profileRoutes);
app.use('/api/gifts', giftRoutes);
app.use('/api/filters', filterRoutes);
app.use('/api/notifications', notificationRoutes);
app.use('/api/audio', audioRoutes);

// MongoDB
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log('MongoDB connected');
    const PORT = process.env.PORT || 5000;
    app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
  })
  .catch((err) => console.error(err));
