import React from 'react';
import styled from 'styled-components';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const Container = styled.div`
  margin: 2rem auto;
  max-width: 1000px;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const SummarySection = styled.div`
  margin-bottom: 2rem;
`;

const ChartContainer = styled.div`
  max-width: 400px;
  margin: 0 auto;
`;

const ResultsSummary = ({ analysis }) => {
  if (!analysis) return null;
  
  // Prepare data for charts
  const statusCounts = analysis.analysis_results.reduce((acc, claim) => {
    acc[claim.verification_status] = (acc[claim.verification_status] || 0) + 1;
    return acc;
  }, {});
  
  const categoryCounts = analysis.analysis_results.reduce((acc, claim) => {
    acc[claim.category] = (acc[claim.category] || 0) + 1;
    return acc;
  }, {});
  
  const statusData = {
    labels: Object.keys(statusCounts),
    datasets: [
      {
        data: Object.values(statusCounts),
        backgroundColor: [
          '#4CAF50', // verified - green
          '#8BC34A', // partially verified - light green
          '#FFC107', // unverified - yellow
          '#F44336'  // debunked - red
        ]
      }
    ]
  };
  
  const categoryData = {
    labels: Object.keys(categoryCounts),
    datasets: [
      {
        data: Object.values(categoryCounts),
        backgroundColor: [
          '#2196F3', '#009688', '#673AB7', '#FF9800', '#E91E63', '#607D8B'
        ]
      }
    ]
  };
  
  return (
    <Container>
      <h2>Analysis Summary</h2>
      
      <SummarySection>
        <h3>Verification Status</h3>
        <ChartContainer>
          <Pie data={statusData} />
        </ChartContainer>
      </SummarySection>
      
      <SummarySection>
        <h3>Claim Categories</h3>
        <ChartContainer>
          <Pie data={categoryData} />
        </ChartContainer>
      </SummarySection>
      
      <SummarySection>
        <h3>Key Findings</h3>
        <div style={{ whiteSpace: 'pre-wrap' }}>{analysis.summary}</div>
      </SummarySection>
    </Container>
  );
};

export default ResultsSummary;