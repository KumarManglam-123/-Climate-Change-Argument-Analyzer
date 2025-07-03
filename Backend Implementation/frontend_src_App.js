import React, { useState } from 'react';
import DebateInput from './components/DebateInput';
import ResultsSummary from './components/ResultsSummary';
import ClaimDetails from './components/ClaimDetails';
import ArgumentVisualization from './components/ArgumentVisualization';
import styled from 'styled-components';

const AppContainer = styled.div`
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  background: #f5f5f5;
  min-height: 100vh;
`;

const Header = styled.header`
  background: #2c3e50;
  color: white;
  padding: 2rem;
  text-align: center;
  margin-bottom: 2rem;
  border-radius: 0 0 8px 8px;
`;

function App() {
  const [analysis, setAnalysis] = useState(null);
  
  return (
    <AppContainer>
      <Header>
        <h1>Climate Debate Analyzer</h1>
        <p>Analyze climate change arguments with AI-powered fact-checking</p>
      </Header>
      
      <DebateInput onAnalysisComplete={setAnalysis} />
      
      {analysis && (
        <>
          <ResultsSummary analysis={analysis} />
          <ArgumentVisualization claims={analysis.analysis_results} />
          <ClaimDetails claims={analysis.analysis_results} />
        </>
      )}
    </AppContainer>
  );
}

export default App;