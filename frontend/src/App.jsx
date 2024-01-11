import { BrowserRouter as Router, Route, Routes, BrowserRouter } from 'react-router-dom';
import HomePage from './HomePage';
import Header from './components/header/header'
import Footer from './components/footer/footer'
import './App.css'

function App() {
  return (
    <Router >
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App
