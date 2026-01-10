import { OAuth2Client } from "google-auth-library";
import jwt from "jsonwebtoken";
import User from "../models/User.js";

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

export const googleAuth = async (req, res) => {
  
    const { idToken, role } = req.body;
  
    if (!idToken || !role) return res.status(400).json({ message: "Role or Token missing" });

    if (!process.env.GOOGLE_CLIENT_ID) {
      console.error("Missing GOOGLE_CLIENT_ID in environment");
      return res.status(500).json({ message: "Server misconfiguration: missing GOOGLE_CLIENT_ID" });
    }
    
    if (!process.env.JWT_SECRET) {
      console.error("Missing JWT_SECRET in environment");
      return res.status(500).json({ message: "Server misconfiguration: missing JWT_SECRET" });
    }

    // 1️⃣ Verify Google token
    let ticket;
    try{
      ticket = await client.verifyIdToken({
        idToken: idToken,
        audience: process.env.GOOGLE_CLIENT_ID,
      });

    } catch(err){
      console.error("Google token verification failed:", err && err.message ? err.message : err);
      return res.status(400).json({ message: "Invalid Google token", error: err.message });
    }
    
  try {
    const payload = ticket.getPayload();

    // 2️⃣ Extract user info
    const { sub, email, name, picture } = payload;

    // 3️⃣ Register or Login
    let user = await User.findOne({ googleId: sub });

    if (!user) {
      user = await User.create({
        googleId: sub,
        name,
        email,
        avatar: picture,
        role: role
      });
    }

    // 4️⃣ Generate JWT (no expiry)
    const token = jwt.sign(
      { id: user._id, email: user.email, role: user.role },
      process.env.JWT_SECRET
    );

    res.json({
      message: "Authenticated",
      user,
      token,
      role,
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server Error", error: err.message });
  }
};
