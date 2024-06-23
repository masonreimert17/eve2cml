import logo from './logo.svg';
import './App.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
function App() {
  return (
    <Navbar className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="#home">Brand link</Navbar.Brand>
        </Container>
      </Navbar>
  );
}

export default App;
