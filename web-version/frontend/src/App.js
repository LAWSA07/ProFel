import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import SplineBackground from './components/SplineBackground';

// Import pages
import Home from './pages/Home';
import GithubProfilePage from './pages/GithubProfilePage';
import JobsPage from './pages/JobsPage';
import MatchingPage from './pages/MatchingPage';
import NotFound from './pages/NotFound';

// Error boundary to catch errors in SplineBackground
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Fallback UI when an error occurs
      return <div className="App">{this.props.children}</div>;
    }

    return this.props.children;
  }
}

function App() {
  return (
    <Router>
      <ErrorBoundary>
        <SplineBackground>
          <div className="App">
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
        </SplineBackground>
      </ErrorBoundary>
    </Router>
  );
}

export default App;
