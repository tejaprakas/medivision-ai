"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { Heart, Mail, Lock, User, Phone, Eye, EyeOff, ArrowRight, Stethoscope } from "lucide-react";
import { authAPI } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import toast from "react-hot-toast";

export default function SignupPage() {
  const router = useRouter();
  const login = useAuthStore((s) => s.login);
  const [step, setStep] = useState<"role" | "form">("role");
  const [role, setRole] = useState<"patient" | "doctor">("patient");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await authAPI.register({
        email,
        password,
        full_name: fullName,
        role,
      });
      const { access_token, refresh_token, user } = res.data;
      login(user, access_token, refresh_token);
      toast.success("Account created successfully!");
      if (user.role === "doctor") router.push("/dashboard/doctor");
      else router.push("/dashboard/patient");
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 via-blue-700 to-cyan-600 p-12 flex-col justify-between relative overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.05)_1px,transparent_1px)] bg-[size:40px_40px]" />
        <div className="relative z-10">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
              <Heart className="w-6 h-6 text-white" fill="white" />
            </div>
            <span className="text-2xl font-bold text-white">MediVision AI</span>
          </Link>
        </div>
        <div className="relative z-10">
          <h2 className="text-4xl font-bold text-white mb-4 leading-tight">Join the Future<br />of Healthcare</h2>
          <p className="text-blue-100 text-lg max-w-md">Get AI-powered heart disease screening, instant medical image analysis, and intelligent health consultations.</p>
          <div className="mt-8 space-y-3">
            {["Free AI-powered analyses", "PDF medical reports", "AI chatbot consultations", "Doctor appointments"].map((f) => (
              <div key={f} className="flex items-center gap-3 text-white/90">
                <div className="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center text-xs">✓</div>
                {f}
              </div>
            ))}
          </div>
        </div>
        <div className="relative z-10">
          <div className="bg-white/10 backdrop-blur rounded-2xl p-4 border border-white/20">
            <p className="text-white/90 text-sm italic">&quot;MediVision AI detected early signs of arrhythmia that I missed. It saved my patient&apos;s life.&quot;</p>
            <p className="text-white/70 text-xs mt-2">— Dr. Rajesh Kumar, Cardiologist</p>
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 flex items-center justify-center p-6 bg-slate-50">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <div className="lg:hidden flex items-center gap-2 mb-8 justify-center">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center">
                <Heart className="w-5 h-5 text-white" fill="white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">MediVision AI</span>
            </Link>
          </div>

          {step === "role" ? (
            <>
              <h1 className="text-2xl font-bold text-slate-900 mb-2">Create your account</h1>
              <p className="text-slate-500 mb-8">Choose how you want to use MediVision AI</p>

              <div className="space-y-4 mb-8">
                <button
                  onClick={() => { setRole("patient"); setStep("form"); }}
                  className={`w-full p-5 rounded-2xl border-2 text-left transition-all hover:shadow-lg group ${
                    "border-blue-500 bg-blue-50"
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center text-2xl">
                      🧑‍⚕️
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900 text-lg">I&apos;m a Patient</h3>
                      <p className="text-sm text-slate-500 mt-1">Get AI analysis of your medical images, track your health, and consult with doctors.</p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => { setRole("doctor"); setStep("form"); }}
                  className={`w-full p-5 rounded-2xl border-2 text-left transition-all hover:shadow-lg group border-slate-200 hover:border-blue-300`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
                      <Stethoscope className="w-6 h-6 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900 text-lg">I&apos;m a Doctor</h3>
                      <p className="text-sm text-slate-500 mt-1">Review AI predictions, manage patients, and provide clinical feedback.</p>
                    </div>
                  </div>
                </button>
              </div>
            </>
          ) : (
            <>
              <button onClick={() => setStep("role")} className="text-sm text-blue-600 hover:text-blue-700 mb-4 flex items-center gap-1">
                ← Back to role selection
              </button>
              <h1 className="text-2xl font-bold text-slate-900 mb-2">
                {role === "patient" ? "Patient Registration" : "Doctor Registration"}
              </h1>
              <p className="text-slate-500 mb-8">Create your {role} account</p>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1.5">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-400" />
                    <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="John Doe" required
                      className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1.5">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-400" />
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required
                      className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1.5">Phone (optional)</label>
                  <div className="relative">
                    <Phone className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-400" />
                    <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+91 98765 43210"
                      className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1.5">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-400" />
                    <input type={showPassword ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Min 8 characters" required minLength={8}
                      className="w-full pl-11 pr-11 py-3 rounded-xl border border-slate-200 bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all" />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                      {showPassword ? <EyeOff className="w-4.5 h-4.5" /> : <Eye className="w-4.5 h-4.5" />}
                    </button>
                  </div>
                </div>
                <button type="submit" disabled={loading}
                  className="w-full py-3.5 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-blue-500/25 hover:-translate-y-0.5 transition-all disabled:opacity-50 flex items-center justify-center gap-2">
                  {loading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <>Create Account <ArrowRight className="w-4 h-4" /></>}
                </button>
              </form>
            </>
          )}

          <p className="text-center text-sm text-slate-500 mt-6">
            Already have an account?{" "}
            <Link href="/login" className="font-semibold text-blue-600 hover:text-blue-700">Sign in</Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
}
