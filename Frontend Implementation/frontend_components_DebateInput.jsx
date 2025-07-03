import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const Container = styled.div`
  margin: 2rem auto;
  max-width: 800px;
`;

const TextArea = styled.textarea`
  width: 100%;
  height: 200px;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 1rem;
`;

const Button = styled.button`
  background-color: #4CAF50;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  
  &:hover {
    background-color: #45a049;
  }
  
  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
`;

const DebateInput = ({ onAnalysisComplete }) => {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Please enter some debate text to analyze');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:8000/analyze/', {
        original_text: text
      });
      onAnalysisComplete(response.data);
    } catch (err) {
      setError('Failed to analyze the debate. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <h2>Enter Climate Debate Text</h2>
      <TextArea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste climate debate transcript or article here..."
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <Button onClick={handleSubmit} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Analyze Debate'}
      </Button>
    </Container>
  );
};

export default DebateInput;