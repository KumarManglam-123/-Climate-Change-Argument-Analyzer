import React from 'react';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';

const Container = styled.div`
  margin: 2rem auto;
  max-width: 1000px;
`;

const ClaimCard = styled.div`
  background: white;
  border-left: 4px solid ${props => {
    switch(props.status) {
      case 'verified': return '#4CAF50';
      case 'partially_verified': return '#8BC34A';
      case 'unverified': return '#FFC107';
      case 'debunked': return '#F44336';
      default: return '#607D8B';
    }
  }};
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 0 4px 4px 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const StatusBadge = styled.span`
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
  background-color: ${props => {
    switch(props.status) {
      case 'verified': return '#4CAF50';
      case 'partially_verified': return '#8BC34A';
      case 'unverified': return '#FFC107';
      case 'debunked': return '#F44336';
      default: return '#607D8B';
    }
  }};
  margin-right: 0.5rem;
`;

const EvidenceList = styled.div`
  margin-top: 1rem;
  padding-left: 1rem;
  border-left: 2px solid #eee;
`;

const EvidenceItem = styled.div`
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f9f9f9;
  border-radius: 4px;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const ClaimDetails = ({ claims }) => {
  if (!claims || claims.length === 0) return null;
  
  return (
    <Container>
      <h2>Detailed Claim Analysis</h2>
      {claims.map((claim, index) => (
        <ClaimCard key={index} status={claim.verification_status}>
          <div>
            <StatusBadge status={claim.verification_status}>
              {claim.verification_status.replace('_', ' ')}
            </StatusBadge>
            <span style={{ fontWeight: 'bold' }}>{claim.category}</span>
            <span style={{ float: 'right' }}>
              Confidence: {(claim.confidence_score * 100).toFixed(0)}%
            </span>
          </div>
          <p style={{ margin: '0.5rem 0' }}>{claim.claim_text}</p>
          
          {claim.supporting_evidence && claim.supporting_evidence.length > 0 && (
            <EvidenceList>
              <h4>Supporting Evidence:</h4>
              {claim.supporting_evidence.map((evidence, i) => (
                <EvidenceItem key={`sup-${i}`}>
                  <strong>{evidence.source}:</strong> {evidence.excerpt}
                  <div style={{ fontSize: '0.8rem', color: '#666' }}>
                    {evidence.reference}
                  </div>
                </EvidenceItem>
              ))}
            </EvidenceList>
          )}
          
          {claim.contradicting_evidence && claim.contradicting_evidence.length > 0 && (
            <EvidenceList>
              <h4>Contradicting Evidence:</h4>
              {claim.contradicting_evidence.map((evidence, i) => (
                <EvidenceItem key={`cont-${i}`}>
                  <strong>{evidence.source}:</strong> {evidence.excerpt}
                  <div style={{ fontSize: '0.8rem', color: '#666' }}>
                    {evidence.reference}
                  </div>
                </EvidenceItem>
              ))}
            </EvidenceList>
          )}
        </ClaimCard>
      ))}
    </Container>
  );
};

export default ClaimDetails;