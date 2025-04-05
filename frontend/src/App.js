import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Import pages
import Home from './pages/Home';
import GithubProfilePage from './pages/GithubProfilePage';
import JobsPage from './pages/JobsPage';
import MatchingPage from './pages/MatchingPage';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Simple gradient background to replace Spline */}
        <div className="fixed top-0 left-0 w-full h-full z-0 pointer-events-none bg-gradient-to-br from-blue-50 to-indigo-100">
          <div className="absolute top-0 left-0 w-96 h-96 bg-blue-200 rounded-full filter blur-3xl opacity-30"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-200 rounded-full filter blur-3xl opacity-30"></div>
        </div>

        {/* Main content */}
        <div className="relative z-10">
          <Navbar />
          <main className="container mx-auto py-4 px-4 sm:px-6 lg:px-8 min-h-screen">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/profiles" element={<GithubProfilePage />} />
              <Route path="/jobs" element={<JobsPage />} />
              <Route path="/matching" element={<MatchingPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </div>
    </Router>
  );
}

export default App;
