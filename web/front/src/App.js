import logo from './logo.svg';
import './App.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import SelectorForm from './components/Selector Form/SelectorForm';
import { useState, useEffect } from 'react';
import { apiGet, downloadFile } from './components/HelperFunctions';
import TableInput from './components/Table-Input/TableInput';

function App() {
  const [backReady, setBackReady] = useState(false)
  
  const [fileDownloadLink, setFileDownloadLink] = useState('')
  // useEffect(() => {
  //   async function fetchData() {
  //     const result = await apiGet('hello');
  //     setHello(result);
  //   }
  //   fetchData();
  // }, []);
 const handleDownloadClick = ()=>{
    downloadFile(fileDownloadLink, 'download.'+fileDownloadLink.split('.').pop())
 }
 const  handleFile=(file)=>{
    const data = new FormData
    data.append('file_from_react', file)
    fetch(window.origin+'/api/ingestFile',{
      method:'post',
      body:data
    }).then(res=>res.json()).then(body=>{
      console.log(body)
      if (body.status === 0){
        console.log("The backend had a oopsies.")
      }
      else{
        let link = window.origin+'/static/'+body['download-url']
        setFileDownloadLink(link)
        setBackReady(true)
        
      }
    })
    
 }
  return (
    <>
      <Navbar className="bg-body-tertiary" data-bs-theme="dark">
        <Navbar.Brand className='ms-3' href="#home">Converter</Navbar.Brand>
      </Navbar>

      <Container>
          <div className='d-flex justify-content-center'>
          <SelectorForm handleFile={handleFile}/>
        </div>
        {backReady && 
      <>
      <div className='mt-4'>
      <TableInput></TableInput>
      </div>
      
      </>
      }
      </Container>
      
    </>
  );
}

export default App;
