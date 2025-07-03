import React from 'react';
import { ForceGraph2D } from 'react-force-graph';
import styled from 'styled-components';

const Container = styled.div`
  margin: 2rem auto;
  max-width: 1000px;
  height: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const ArgumentVisualization = ({ claims }) => {
  if (!claims || claims.length === 0) return null;
  
  // Prepare graph data
  const nodes = claims.map((claim, idx) => ({
    id: idx,
    name: claim.claim_text.substring(0, 50) + '...',
    category: claim.category,
    status: claim.verification_status,
    val: claim.confidence_score * 10
  }));
  
  // Create links between claims that share the same category
  const links = [];
  const categoryMap = {};
  
  claims.forEach((claim, idx) => {
    if (!categoryMap[claim.category]) {
      categoryMap[claim.category] = [];
    }
    categoryMap[claim.category].push(idx);
  });
  
  Object.values(categoryMap).forEach(categoryNodes => {
    if (categoryNodes.length > 1) {
      for (let i = 0; i < categoryNodes.length - 1; i++) {
        links.push({
          source: categoryNodes[i],
          target: categoryNodes[i + 1],
          value: 0.5
        });
      }
    }
  });
  
  const graphData = { nodes, links };
  
  const nodeColor = node => {
    switch(node.status) {
      case 'verified': return '#4CAF50';
      case 'partially_verified': return '#8BC34A';
      case 'unverified': return '#FFC107';
      case 'debunked': return '#F44336';
      default: return '#607D8B';
    }
  };
  
  return (
    <Container>
      <h2 style={{ padding: '1rem' }}>Argument Network</h2>
      <ForceGraph2D
        graphData={graphData}
        nodeLabel={node => `
          <div style="padding: 8px; background: white; border-radius: 4px; border: 1px solid #eee;">
            <strong>${node.name}</strong><br/>
            <span>Category: ${node.category}</span><br/>
            <span>Status: ${node.status.replace('_', ' ')}</span>
          </div>
        `}
        nodeColor={nodeColor}
        linkColor={() => 'rgba(0, 0, 0, 0.2)'}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.name;
          const fontSize = 12 / globalScale;
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = 'black';
          ctx.fillText(label, node.x, node.y);
        }}
      />
    </Container>
  );
};

export default ArgumentVisualization;