"use client";

import { useState, useEffect, useRef } from "react";
import { motion, useScroll, useTransform, AnimatePresence } from "framer-motion";
import {
  Heart, Brain, Shield, Upload, MessageSquare, FileText, Calendar,
  Activity, Scan, Stethoscope, Zap, Users, TrendingUp, CheckCircle,
  ChevronRight, Play, Star, ArrowRight, Menu, X, Sun, Moon,
  Clock, Award, Globe, Lock, Eye, BarChart3, Bell, Settings,
  UserCheck, HeartPulse, Microscope, Pill, Phone
} from "lucide-react";

// ============================================================
// NAVBAR
// ============================================================
function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { label: "Features", href: "#features" },
    { label: "How It Works", href: "#workflow" },
    { label: "AI Models", href: "#models" },
    { label: "Dashboard", href: "#dashboard" },
    { label: "Testimonials", href: "#testimonials" },
    { label: "Pricing", href: "#pricing" },
  ];

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled
          ? "bg-white/80 dark:bg-slate-900/80 backdrop-blur-2xl shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20 border-b border-slate-200/50 dark:border-slate-700/50"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2.5 group">
            <div className="relative w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-shadow">
              <Heart className="w-5 h-5 text-white" fill="white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              MediVision AI
            </span>
          </a>

          {/* Desktop Nav */}
          <div className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-950/30 transition-all"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Actions */}
          <div className="hidden lg:flex items-center gap-3">
            <button
              onClick={() => setIsDark(!isDark)}
              className="p-2 rounded-xl text-slate-500 hover:text-slate-700 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all"
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <a
              href="#login"
              className="px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Sign In
            </a>
            <a
              href="#signup"
              className="px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-cyan-500 rounded-xl hover:shadow-lg hover:shadow-blue-500/25 hover:-translate-y-0.5 transition-all"
            >
              Get Started Free
            </a>
          </div>

          {/* Mobile Toggle */}
          <button
            onClick={() => setIsMobileOpen(!isMobileOpen)}
            className="lg:hidden p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            {isMobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden bg-white/95 dark:bg-slate-900/95 backdrop-blur-2xl border-b border-slate-200/50 dark:border-slate-700/50"
          >
            <div className="px-4 py-4 space-y-1">
              {navLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  onClick={() => setIsMobileOpen(false)}
                  className="block px-4 py-3 text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 rounded-xl hover:bg-blue-50 dark:hover:bg-blue-950/30 transition-all"
                >
                  {link.label}
                </a>
              ))}
              <div className="pt-3 border-t border-slate-200 dark:border-slate-700 flex flex-col gap-2">
                <a href="#login" className="px-4 py-3 text-sm font-medium text-center text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl">
                  Sign In
                </a>
                <a href="#signup" className="px-4 py-3 text-sm font-semibold text-center text-white bg-gradient-to-r from-blue-600 to-cyan-500 rounded-xl">
                  Get Started Free
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
}

// ============================================================
// HERO SECTION
// ============================================================
function HeroSection() {
  const [counter, setCounter] = useState({ patients: 0, analyses: 0, accuracy: 0 });

  useEffect(() => {
    const timer = setInterval(() => {
      setCounter((prev) => ({
        patients: Math.min(prev.patients + 1247, 50000),
        analyses: Math.min(prev.analyses + 3891, 125000),
        accuracy: Math.min(prev.accuracy + 0.2, 97.8),
      }));
    }, 30);
    return () => clearInterval(timer);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center overflow-hidden bg-gradient-to-b from-slate-50 via-blue-50/30 to-white dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-blue-500/5 to-cyan-500/5 rounded-full blur-3xl" />
        {/* Grid pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.03)_1px,transparent_1px)] bg-[size:60px_60px]" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16 lg:pt-32 lg:pb-24">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 dark:bg-blue-950/50 border border-blue-200 dark:border-blue-800/50 mb-6"
            >
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-500 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-600" />
              </span>
              <span className="text-sm font-semibold text-blue-700 dark:text-blue-300">
                AI-Powered Healthcare Platform
              </span>
            </motion.div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-[1.1] mb-6">
              AI-Powered{" "}
              <span className="bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600 bg-clip-text text-transparent">
                Heart Disease
              </span>{" "}
              Detection & Medical Assistant
            </h1>

            <p className="text-lg sm:text-xl text-slate-600 dark:text-slate-400 leading-relaxed mb-8 max-w-xl">
              Upload <strong className="text-slate-700 dark:text-slate-200">ECG, MRI, CT Scan or X-Ray</strong> images
              and receive intelligent AI-powered analysis, risk assessment, and medical explanations.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap gap-3 mb-10">
              <a
                href="#signup"
                className="group inline-flex items-center gap-2 px-7 py-4 text-base font-semibold text-white bg-gradient-to-r from-blue-600 to-cyan-500 rounded-2xl shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 hover:-translate-y-1 transition-all"
              >
                <Upload className="w-5 h-5" />
                Start Analysis
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </a>
              <a
                href="#chatbot"
                className="group inline-flex items-center gap-2 px-7 py-4 text-base font-semibold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
              >
                <MessageSquare className="w-5 h-5 text-cyan-500" />
                Talk to AI
              </a>
              <a
                href="#appointments"
                className="group inline-flex items-center gap-2 px-7 py-4 text-base font-semibold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
              >
                <Calendar className="w-5 h-5 text-green-500" />
                Book Consultation
              </a>
            </div>

            {/* Stats */}
            <div className="flex flex-wrap gap-8">
              {[
                { value: "50K+", label: "Patients Screened", icon: Users },
                { value: "125K+", label: "AI Analyses", icon: Brain },
                { value: "97.8%", label: "Accuracy Rate", icon: Award },
              ].map((stat) => (
                <div key={stat.label} className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-950/50 flex items-center justify-center">
                    <stat.icon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div>
                    <div className="text-xl font-bold text-slate-900 dark:text-white">{stat.value}</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">{stat.label}</div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Right Visual — Floating Cards */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="relative hidden lg:block"
          >
            {/* Main Card */}
            <div className="relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-2xl rounded-3xl shadow-2xl border border-slate-200/50 dark:border-slate-700/50 p-6">
              {/* Mock Dashboard */}
              <div className="flex items-center gap-3 mb-5">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                <div className="w-3 h-3 rounded-full bg-green-400" />
                <div className="flex-1 h-6 bg-slate-100 dark:bg-slate-700 rounded-lg ml-2" />
              </div>

              {/* ECG Visualization */}
              <div className="bg-slate-50 dark:bg-slate-900/50 rounded-2xl p-4 mb-4">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">ECG Analysis</span>
                  <span className="text-xs px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-full font-medium">Live</span>
                </div>
                <svg viewBox="0 0 400 100" className="w-full h-20">
                  <motion.path
                    d="M0,50 Q25,20 50,50 T100,50 T150,50 T200,50 T250,50 T300,50 T350,50 T400,50"
                    fill="none"
                    stroke="url(#ecgGradient)"
                    strokeWidth="2"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  />
                  <defs>
                    <linearGradient id="ecgGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#2563EB" />
                      <stop offset="100%" stopColor="#06B6D4" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>

              {/* Result Card */}
              <div className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-950/30 dark:to-cyan-950/30 rounded-2xl p-4 border border-blue-100 dark:border-blue-900/50">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm text-slate-500 dark:text-slate-400">Prediction</div>
                    <div className="text-lg font-bold text-slate-900 dark:text-white">Analysis Complete</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500 dark:text-slate-400">Confidence</div>
                    <div className="text-lg font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">97.3%</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Floating Cards */}
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              className="absolute -top-6 -right-6 bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200/50 dark:border-slate-700/50 p-4 flex items-center gap-3"
            >
              <div className="w-10 h-10 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div className="text-sm font-semibold text-slate-900 dark:text-white">AI Verified</div>
                <div className="text-xs text-slate-500 dark:text-slate-400">Report ready</div>
              </div>
            </motion.div>

            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
              className="absolute -bottom-4 -left-6 bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200/50 dark:border-slate-700/50 p-4 flex items-center gap-3"
            >
              <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <Shield className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div className="text-sm font-semibold text-slate-900 dark:text-white">HIPAA Secure</div>
                <div className="text-xs text-slate-500 dark:text-slate-400">Encrypted data</div>
              </div>
            </motion.div>

            <motion.div
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
              className="absolute top-1/2 -right-10 bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200/50 dark:border-slate-700/50 p-4 flex items-center gap-3"
            >
              <div className="w-10 h-10 rounded-xl bg-cyan-100 dark:bg-cyan-900/30 flex items-center justify-center">
                <HeartPulse className="w-5 h-5 text-cyan-600" />
              </div>
              <div>
                <div className="text-sm font-semibold text-slate-900 dark:text-white">Heart Score</div>
                <div className="text-xs font-bold text-cyan-600">Good</div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="absolute bottom-0 left-0 right-0 bg-amber-50 dark:bg-amber-950/20 border-t border-amber-200/50 dark:border-amber-900/30 py-3 px-4">
        <p className="text-center text-xs text-amber-700 dark:text-amber-400 max-w-4xl mx-auto">
          ⚠️ <strong>Medical Disclaimer:</strong> AI-generated results are for educational and preliminary screening purposes only. Always consult a qualified healthcare professional.
        </p>
      </div>
    </section>
  );
}

// ============================================================
// FEATURES SECTION
// ============================================================
function FeaturesSection() {
  const features = [
    { icon: Activity, title: "ECG Analysis", desc: "Analyze electrocardiogram images for arrhythmia, AFib, and other heart rhythm disorders.", color: "blue" },
    { icon: Scan, title: "MRI Analysis", desc: "Detect structural heart abnormalities, cardiomyopathy, and valve disorders from MRI scans.", color: "purple" },
    { icon: Microscope, title: "CT Scan Analysis", desc: "Identify coronary artery disease, calcifications, and structural anomalies.", color: "cyan" },
    { icon: Eye, title: "X-Ray Analysis", desc: "Screen for cardiomegaly, lung conditions, and chest-related abnormalities.", color: "green" },
    { icon: HeartPulse, title: "Heart Disease Prediction", desc: "Ensemble AI models predict heart disease risk with confidence scores.", color: "red" },
    { icon: MessageSquare, title: "AI Medical Chatbot", desc: "Powered by BioGPT — explain reports, answer questions, provide guidance.", color: "indigo" },
    { icon: FileText, title: "PDF Report Generator", desc: "Generate professional medical reports with findings and recommendations.", color: "orange" },
    { icon: Clock, title: "Patient History Tracking", desc: "Track all analyses, reports, and health trends over time.", color: "teal" },
    { icon: Stethoscope, title: "Doctor Dashboard", desc: "Manage patients, review AI predictions, and provide clinical notes.", color: "emerald" },
    { icon: Calendar, title: "Appointment Scheduling", desc: "Book consultations, video calls, and in-person appointments.", color: "sky" },
    { icon: Phone, title: "Voice Assistant", desc: "Speech-to-text and text-to-speech for hands-free interaction.", color: "violet" },
    { icon: Bell, title: "Emergency Alert System", desc: "Critical findings trigger immediate notifications and alerts.", color: "rose" },
  ];

  const colorMap: Record<string, string> = {
    blue: "from-blue-500 to-blue-600 shadow-blue-500/25",
    purple: "from-purple-500 to-purple-600 shadow-purple-500/25",
    cyan: "from-cyan-500 to-cyan-600 shadow-cyan-500/25",
    green: "from-green-500 to-green-600 shadow-green-500/25",
    red: "from-red-500 to-red-600 shadow-red-500/25",
    indigo: "from-indigo-500 to-indigo-600 shadow-indigo-500/25",
    orange: "from-orange-500 to-orange-600 shadow-orange-500/25",
    teal: "from-teal-500 to-teal-600 shadow-teal-500/25",
    emerald: "from-emerald-500 to-emerald-600 shadow-emerald-500/25",
    sky: "from-sky-500 to-sky-600 shadow-sky-500/25",
    violet: "from-violet-500 to-violet-600 shadow-violet-500/25",
    rose: "from-rose-500 to-rose-600 shadow-rose-500/25",
  };

  return (
    <section id="features" className="py-20 lg:py-32 bg-white dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            Platform Features
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            Complete AI Healthcare{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Platform
            </span>
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Everything you need for AI-powered heart disease detection, patient management, and medical consultations.
          </p>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.05 }}
              className="group relative bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/50 dark:border-slate-800 p-6 hover:shadow-xl hover:shadow-slate-200/50 dark:hover:shadow-slate-900/50 hover:-translate-y-1 transition-all duration-300"
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorMap[feature.color]} shadow-lg flex items-center justify-center mb-4`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ============================================================
// WORKFLOW SECTION
// ============================================================
function WorkflowSection() {
  const steps = [
    { num: "01", icon: Upload, title: "Upload Image", desc: "Upload ECG, MRI, CT Scan or X-Ray images via drag & drop.", detail: "Supports JPG, PNG, DICOM formats" },
    { num: "02", icon: Brain, title: "AI Analysis", desc: "ViT + ResNet50 ensemble models analyze your image.", detail: "Feature extraction & pattern recognition" },
    { num: "03", icon: BarChart3, title: "Get Results", desc: "Receive prediction, confidence score, and risk assessment.", detail: "Low / Moderate / High / Critical" },
    { num: "04", icon: MessageSquare, title: "AI Explanation", desc: "Chatbot explains findings and answers your questions.", detail: "Powered by BioGPT & BioBERT" },
    { num: "05", icon: FileText, title: "Download Report", desc: "Generate and download a professional PDF medical report.", detail: "Share with your doctor" },
  ];

  return (
    <section id="workflow" className="py-20 lg:py-32 bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            How It Works
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            5-Step AI{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Analysis Pipeline
            </span>
          </h2>
        </motion.div>

        <div className="relative">
          {/* Connection Line */}
          <div className="hidden lg:block absolute top-24 left-[10%] right-[10%] h-0.5 bg-gradient-to-r from-blue-500 via-cyan-500 to-blue-500 opacity-20" />

          <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-6">
            {steps.map((step, i) => (
              <motion.div
                key={step.num}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="relative text-center group"
              >
                <div className="relative w-20 h-20 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center shadow-xl shadow-blue-500/25 group-hover:shadow-blue-500/40 group-hover:scale-110 transition-all">
                  <step.icon className="w-9 h-9 text-white" />
                  <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-white dark:bg-slate-800 text-xs font-bold text-blue-600 flex items-center justify-center shadow-md border border-slate-200 dark:border-slate-700">
                    {step.num}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">{step.title}</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">{step.desc}</p>
                <p className="text-xs text-blue-600 dark:text-blue-400 font-medium">{step.detail}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

// ============================================================
// AI MODELS SECTION
// ============================================================
function ModelsSection() {
  const imageModels = [
    { name: "Vision Transformer (ViT)", org: "Google", task: "Medical image classification with attention mechanisms", color: "blue" },
    { name: "ResNet50", org: "Microsoft", task: "Deep residual learning for image recognition", color: "purple" },
    { name: "EfficientNet", org: "Google", task: "Scalable and efficient image classification", color: "green" },
    { name: "Custom CNN", task: "Purpose-built architecture for medical imaging", color: "cyan" },
  ];

  const nlpModels = [
    { name: "BioGPT", org: "Microsoft", task: "Medical text generation & report explanation", color: "indigo" },
    { name: "BioBERT", org: "DMIS Lab", task: "Clinical NLP & medical entity recognition", color: "teal" },
    { name: "MedAlpaca", task: "Medical conversational AI for patient Q&A", color: "orange" },
  ];

  return (
    <section id="models" className="py-20 lg:py-32 bg-white dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            AI Models
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            State-of-the-Art{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              AI Models
            </span>
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Right tool for the right job — Vision models for images, Language models for text.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Image Models */}
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/20 dark:to-cyan-950/20 rounded-3xl p-8 border border-blue-100 dark:border-blue-900/50">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
                <Eye className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Image Analysis Models</h3>
                <p className="text-sm text-slate-500">For ECG, MRI, CT Scan, X-Ray</p>
              </div>
            </div>
            <div className="space-y-4">
              {imageModels.map((model) => (
                <div key={model.name} className="bg-white dark:bg-slate-800/50 rounded-xl p-4 border border-slate-200/50 dark:border-slate-700/50">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="font-semibold text-slate-900 dark:text-white">{model.name}</h4>
                    {model.org && (
                      <span className="text-xs px-2 py-0.5 bg-blue-100 dark:bg-blue-950 text-blue-600 dark:text-blue-400 rounded-full">{model.org}</span>
                    )}
                  </div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">{model.task}</p>
                </div>
              ))}
            </div>
          </div>

          {/* NLP Models */}
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-950/20 dark:to-purple-950/20 rounded-3xl p-8 border border-indigo-100 dark:border-indigo-900/50">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center">
                <MessageSquare className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Language Models</h3>
                <p className="text-sm text-slate-500">For reports, Q&A, explanations</p>
              </div>
            </div>
            <div className="space-y-4">
              {nlpModels.map((model) => (
                <div key={model.name} className="bg-white dark:bg-slate-800/50 rounded-xl p-4 border border-slate-200/50 dark:border-slate-700/50">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="font-semibold text-slate-900 dark:text-white">{model.name}</h4>
                    {model.org && (
                      <span className="text-xs px-2 py-0.5 bg-indigo-100 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 rounded-full">{model.org}</span>
                    )}
                  </div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">{model.task}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ============================================================
// TECH STACK SECTION
// ============================================================
function TechStackSection() {
  const stacks = [
    { category: "Frontend", techs: ["Next.js 14", "TypeScript", "Tailwind CSS", "Framer Motion"] },
    { category: "Backend", techs: ["FastAPI", "Python 3.11+", "JWT Auth", "WebSocket"] },
    { category: "AI/ML", techs: ["PyTorch", "Hugging Face", "OpenCV", "ViT / ResNet50"] },
    { category: "Database", techs: ["MongoDB", "Redis", "Cloudinary", "AWS S3"] },
    { category: "Security", techs: ["HTTPS", "HIPAA-style", "Encryption", "Rate Limiting"] },
    { category: "Deployment", techs: ["Docker", "AWS", "Render", "Hugging Face Spaces"] },
  ];

  return (
    <section className="py-20 lg:py-32 bg-slate-50 dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            Technology Stack
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            Built with{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Modern Tech
            </span>
          </h2>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {stacks.map((stack, i) => (
            <motion.div
              key={stack.category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/50 dark:border-slate-700 p-6"
            >
              <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4">{stack.category}</h3>
              <div className="flex flex-wrap gap-2">
                {stack.techs.map((tech) => (
                  <span
                    key={tech}
                    className="px-3 py-1.5 text-xs font-medium text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-700 rounded-lg"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ============================================================
// DASHBOARD PREVIEW
// ============================================================
function DashboardPreview() {
  return (
    <section id="dashboard" className="py-20 lg:py-32 bg-white dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            Dashboards
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            Role-Based{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Dashboards
            </span>
          </h2>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-6">
          {[
            {
              role: "Patient",
              color: "blue",
              features: ["Health Score", "Recent Reports", "Uploaded Images", "Chat History", "Appointments", "Notifications"],
              metrics: [
                { label: "Health Score", value: "85/100", icon: Heart },
                { label: "Reports", value: "12", icon: FileText },
                { label: "Analyses", value: "8", icon: Brain },
              ],
            },
            {
              role: "Doctor",
              color: "emerald",
              features: ["Assigned Patients", "Pending Reviews", "AI Predictions", "Appointment Requests"],
              metrics: [
                { label: "Patients", value: "48", icon: Users },
                { label: "Reviews", value: "7", icon: CheckCircle },
                { label: "Rating", value: "4.9", icon: Star },
              ],
            },
            {
              role: "Admin",
              color: "purple",
              features: ["Total Users", "Revenue Metrics", "AI Usage Analytics", "System Health"],
              metrics: [
                { label: "Users", value: "2,450", icon: Users },
                { label: "Reports", value: "8,920", icon: FileText },
                { label: "Uptime", value: "99.9%", icon: TrendingUp },
              ],
            },
          ].map((dashboard, i) => (
            <motion.div
              key={dashboard.role}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className={`rounded-3xl border-2 p-6 ${
                dashboard.color === "blue"
                  ? "border-blue-200 dark:border-blue-900 bg-gradient-to-b from-blue-50 to-white dark:from-blue-950/30 dark:to-slate-900"
                  : dashboard.color === "emerald"
                  ? "border-emerald-200 dark:border-emerald-900 bg-gradient-to-b from-emerald-50 to-white dark:from-emerald-950/30 dark:to-slate-900"
                  : "border-purple-200 dark:border-purple-900 bg-gradient-to-b from-purple-50 to-white dark:from-purple-950/30 dark:to-slate-900"
              }`}
            >
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4">{dashboard.role} Dashboard</h3>
              <div className="grid grid-cols-3 gap-3 mb-5">
                {dashboard.metrics.map((metric) => (
                  <div key={metric.label} className="bg-white dark:bg-slate-800 rounded-xl p-3 text-center border border-slate-200/50 dark:border-slate-700">
                    <metric.icon className={`w-4 h-4 mx-auto mb-1 ${
                      dashboard.color === "blue" ? "text-blue-500" : dashboard.color === "emerald" ? "text-emerald-500" : "text-purple-500"
                    }`} />
                    <div className="text-lg font-bold text-slate-900 dark:text-white">{metric.value}</div>
                    <div className="text-[10px] text-slate-500">{metric.label}</div>
                  </div>
                ))}
              </div>
              <div className="space-y-2">
                {dashboard.features.map((feature) => (
                  <div key={feature} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                    <CheckCircle className={`w-4 h-4 ${
                      dashboard.color === "blue" ? "text-blue-500" : dashboard.color === "emerald" ? "text-emerald-500" : "text-purple-500"
                    }`} />
                    {feature}
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ============================================================
// TESTIMONIALS
// ============================================================
function TestimonialsSection() {
  const testimonials = [
    {
      name: "Dr. Rajesh Kumar",
      role: "Cardiologist, AIIMS Delhi",
      text: "MediVision AI has transformed how I screen patients. The AI analysis is incredibly accurate and saves me hours of preliminary work.",
      rating: 5,
    },
    {
      name: "Priya Sharma",
      role: "Patient",
      text: "I was able to get a preliminary heart screening from home. The AI chatbot explained everything in simple terms. Highly recommended!",
      rating: 5,
    },
    {
      name: "Dr. Ananya Reddy",
      role: "Radiologist, Apollo Hospitals",
      text: "The ensemble model approach gives me confidence in the predictions. The PDF reports are professional and easy to share.",
      rating: 5,
    },
  ];

  return (
    <section id="testimonials" className="py-20 lg:py-32 bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            Testimonials
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            Trusted by{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Healthcare Professionals
            </span>
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/50 dark:border-slate-700 p-6 shadow-lg"
            >
              <div className="flex gap-1 mb-4">
                {Array.from({ length: t.rating }).map((_, j) => (
                  <Star key={j} className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                ))}
              </div>
              <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed mb-5">"{t.text}"</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold text-sm">
                  {t.name.charAt(0)}
                </div>
                <div>
                  <div className="text-sm font-semibold text-slate-900 dark:text-white">{t.name}</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400">{t.role}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ============================================================
// PRICING SECTION
// ============================================================
function PricingSection() {
  const plans = [
    {
      name: "Free",
      price: "₹0",
      period: "forever",
      features: ["3 AI analyses/month", "Basic PDF reports", "AI chatbot access", "Patient dashboard"],
      cta: "Get Started",
      popular: false,
    },
    {
      name: "Pro",
      price: "₹999",
      period: "/month",
      features: ["Unlimited AI analyses", "Advanced PDF reports", "Priority chatbot", "Doctor consultations", "Appointment booking", "Analytics dashboard"],
      cta: "Start Free Trial",
      popular: true,
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "pricing",
      features: ["Everything in Pro", "Custom AI models", "API access", "White-label solution", "Dedicated support", "HIPAA compliance"],
      cta: "Contact Sales",
      popular: false,
    },
  ];

  return (
    <section id="pricing" className="py-20 lg:py-32 bg-slate-50 dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-1.5 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/50 rounded-full mb-4">
            Pricing
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 dark:text-white mb-4">
            Simple, Transparent{" "}
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Pricing
            </span>
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className={`relative rounded-3xl p-8 ${
                plan.popular
                  ? "bg-gradient-to-b from-blue-600 to-cyan-500 text-white shadow-2xl shadow-blue-500/25 scale-105"
                  : "bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700"
              }`}
            >
              {plan.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 text-xs font-bold text-blue-600 bg-yellow-400 rounded-full">
                  Most Popular
                </span>
              )}
              <h3 className={`text-lg font-bold mb-2 ${plan.popular ? "text-white" : "text-slate-900 dark:text-white"}`}>
                {plan.name}
              </h3>
              <div className="flex items-baseline gap-1 mb-6">
                <span className={`text-4xl font-extrabold ${plan.popular ? "text-white" : "text-slate-900 dark:text-white"}`}>
                  {plan.price}
                </span>
                <span className={`text-sm ${plan.popular ? "text-blue-100" : "text-slate-500"}`}>
                  {plan.period}
                </span>
              </div>
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-2 text-sm">
                    <CheckCircle className={`w-4 h-4 flex-shrink-0 ${plan.popular ? "text-blue-200" : "text-blue-500"}`} />
                    <span className={plan.popular ? "text-blue-50" : "text-slate-600 dark:text-slate-300"}>{feature}</span>
                  </li>
                ))}
              </ul>
              <a
                href="#signup"
                className={`block text-center py-3 rounded-xl font-semibold text-sm transition-all ${
                  plan.popular
                    ? "bg-white text-blue-600 hover:shadow-lg"
                    : "bg-gradient-to-r from-blue-600 to-cyan-500 text-white hover:shadow-lg hover:shadow-blue-500/25"
                }`}
              >
                {plan.cta}
              </a>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ============================================================
// CTA SECTION
// ============================================================
function CTASection() {
  return (
    <section className="py-20 lg:py-32 bg-gradient-to-r from-blue-600 via-blue-700 to-cyan-600 relative overflow-hidden">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:40px_40px]" />
      <div className="absolute -top-40 -right-40 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
      <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl" />

      <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white mb-6">
            Ready to Transform Healthcare with AI?
          </h2>
          <p className="text-lg text-blue-100 mb-10 max-w-2xl mx-auto">
            Join thousands of healthcare professionals and patients using MediVision AI for faster, smarter heart disease detection.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="#signup"
              className="group inline-flex items-center gap-2 px-8 py-4 text-base font-semibold text-blue-600 bg-white rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all"
            >
              Get Started Free
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>
            <a
              href="#demo"
              className="inline-flex items-center gap-2 px-8 py-4 text-base font-semibold text-white border-2 border-white/30 rounded-2xl hover:bg-white/10 transition-all"
            >
              <Play className="w-4 h-4" />
              Watch Demo
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

// ============================================================
// FOOTER
// ============================================================
function Footer() {
  const links = {
    Product: ["Features", "Pricing", "AI Models", "API Docs", "Integrations"],
    Company: ["About", "Blog", "Careers", "Press", "Contact"],
    Resources: ["Documentation", "Help Center", "Community", "Status", "Changelog"],
    Legal: ["Privacy Policy", "Terms of Service", "HIPAA Compliance", "GDPR", "Cookie Policy"],
  };

  return (
    <footer className="bg-slate-950 text-slate-400 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid sm:grid-cols-2 lg:grid-cols-6 gap-8 mb-12">
          <div className="lg:col-span-2">
            <a href="#" className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center">
                <Heart className="w-5 h-5 text-white" fill="white" />
              </div>
              <span className="text-xl font-bold text-white">MediVision AI</span>
            </a>
            <p className="text-sm leading-relaxed mb-4 max-w-xs">
              AI-powered heart disease detection and medical image analysis platform. Transforming healthcare with artificial intelligence.
            </p>
            <div className="flex gap-3">
              {["twitter", "linkedin", "github", "youtube"].map((social) => (
                <a
                  key={social}
                  href="#"
                  className="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                >
                  <Globe className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {Object.entries(links).map(([category, items]) => (
            <div key={category}>
              <h4 className="text-sm font-semibold text-white mb-4">{category}</h4>
              <ul className="space-y-2.5">
                {items.map((item) => (
                  <li key={item}>
                    <a href="#" className="text-sm hover:text-white transition-colors">{item}</a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-slate-800 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm">© 2024 MediVision AI. All rights reserved.</p>
          <p className="text-xs text-amber-400">
            ⚠️ AI results are for preliminary screening only. Always consult a healthcare professional.
          </p>
        </div>
      </div>
    </footer>
  );
}

// ============================================================
// MAIN PAGE EXPORT
// ============================================================
export default function Home() {
  return (
    <main className="min-h-screen bg-white dark:bg-slate-950">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <WorkflowSection />
      <ModelsSection />
      <TechStackSection />
      <DashboardPreview />
      <TestimonialsSection />
      <PricingSection />
      <CTASection />
      <Footer />
    </main>
  );
}
