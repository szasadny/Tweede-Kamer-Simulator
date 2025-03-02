// Configuration
const API_URL = 'http://localhost:8000/api/v1';

// DOM Elements
const proposalsContainer = document.getElementById('proposals-container');
const partiesContainer = document.getElementById('parties-container');
const membersContainer = document.getElementById('members-container');
const debatesContainer = document.getElementById('debates-container');
const detailView = document.getElementById('detail-view');
const detailContent = document.getElementById('detail-content');
const backBtn = document.getElementById('back-btn');
const newProposalBtn = document.getElementById('new-proposal-btn');

// Navigation
document.getElementById('nav-proposals').addEventListener('click', (e) => {
    e.preventDefault();
    showSection(proposalsContainer);
    loadProposals();
});

document.getElementById('nav-parties').addEventListener('click', (e) => {
    e.preventDefault();
    showSection(partiesContainer);
    loadParties();
});

document.getElementById('nav-members').addEventListener('click', (e) => {
    e.preventDefault();
    showSection(membersContainer);
    loadMembers();
});

document.getElementById('nav-debates').addEventListener('click', (e) => {
    e.preventDefault();
    showSection(debatesContainer);
    loadDebates();
});

backBtn.addEventListener('click', () => {
    detailView.classList.add('d-none');
    document.querySelectorAll('.content-section').forEach(section => {
        if (!section.classList.contains('d-none')) {
            section.classList.remove('d-none');
        }
    });
});

newProposalBtn.addEventListener('click', () => {
    showProposalForm();
});

// Helper Functions
function showSection(section) {
    document.querySelectorAll('.content-section').forEach(s => s.classList.add('d-none'));
    detailView.classList.add('d-none');
    section.classList.remove('d-none');
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    if (section === proposalsContainer) document.getElementById('nav-proposals').classList.add('active');
    if (section === partiesContainer) document.getElementById('nav-parties').classList.add('active');
    if (section === membersContainer) document.getElementById('nav-members').classList.add('active');
    if (section === debatesContainer) document.getElementById('nav-debates').classList.add('active');
}

function showDetail(content) {
    document.querySelectorAll('.content-section').forEach(s => s.classList.add('d-none'));
    detailContent.innerHTML = content;
    detailView.classList.remove('d-none');
}

// API Functions
async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

async function postData(endpoint, data) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Post error:', error);
        return null;
    }
}

// Load Data Functions
async function loadProposals() {
    const proposals = await fetchData('/proposals/');
    const proposalsList = document.getElementById('proposals-list');
    proposalsList.innerHTML = '';
    
    if (proposals && proposals.length > 0) {
        proposals.forEach(proposal => {
            const item = document.createElement('a');
            item.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <h5>${proposal.title}</h5>
                    <span class="badge bg-primary">${proposal.status}</span>
                </div>
                <button class="btn btn-sm btn-info view-proposal" data-id="${proposal.id}">View</button>
            `;
            proposalsList.appendChild(item);
            
            item.querySelector('.view-proposal').addEventListener('click', () => {
                loadProposalDetail(proposal.id);
            });
        });
    } else {
        proposalsList.innerHTML = '<div class="alert alert-info">No proposals found.</div>';
    }
}

async function loadParties() {
    const parties = await fetchData('/parties/');
    const partiesList = document.getElementById('parties-list');
    partiesList.innerHTML = '';
    
    if (parties && parties.length > 0) {
        parties.forEach(party => {
            const item = document.createElement('a');
            item.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <h5>${party.name} (${party.abbreviation})</h5>
                    <p>${party.ideology}</p>
                </div>
                <button class="btn btn-sm btn-info view-party" data-id="${party.id}">View</button>
            `;
            partiesList.appendChild(item);
            
            item.querySelector('.view-party').addEventListener('click', () => {
                loadPartyDetail(party.id);
            });
        });
    } else {
        partiesList.innerHTML = '<div class="alert alert-info">No parties found.</div>';
    }
}

async function loadMembers() {
    const members = await fetchData('/members/');
    const membersList = document.getElementById('members-list');
    membersList.innerHTML = '';
    
    if (members && members.length > 0) {
        members.forEach(member => {
            const item = document.createElement('a');
            item.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <h5>${member.name}</h5>
                    <p>Party ID: ${member.party_id}</p>
                </div>
                <button class="btn btn-sm btn-info view-member" data-id="${member.id}">View</button>
            `;
            membersList.appendChild(item);
            
            item.querySelector('.view-member').addEventListener('click', () => {
                loadMemberDetail(member.id);
            });
        });
    } else {
        membersList.innerHTML = '<div class="alert alert-info">No members found.</div>';
    }
}

async function loadDebates() {
    const debates = await fetchData('/debates/');
    const debatesList = document.getElementById('debates-list');
    debatesList.innerHTML = '';
    
    if (debates && debates.length > 0) {
        debates.forEach(debate => {
            const item = document.createElement('a');
            item.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <h5>${debate.title}</h5>
                    <p>Proposal ID: ${debate.proposal_id}</p>
                </div>
                <button class="btn btn-sm btn-info view-debate" data-id="${debate.id}">View</button>
            `;
            debatesList.appendChild(item);
            
            item.querySelector('.view-debate').addEventListener('click', () => {
                loadDebateDetail(debate.id);
            });
        });
    } else {
        debatesList.innerHTML = '<div class="alert alert-info">No debates found.</div>';
    }
}

// Detail Functions
async function loadProposalDetail(id) {
    const proposal = await fetchData(`/proposals/${id}`);
    if (!proposal) return;
    
    let statusBadge = '';
    switch (proposal.status) {
        case 'draft': statusBadge = '<span class="badge bg-secondary">Draft</span>'; break;
        case 'submitted': statusBadge = '<span class="badge bg-primary">Submitted</span>'; break;
        case 'debating': statusBadge = '<span class="badge bg-info">Debating</span>'; break;
        case 'voting': statusBadge = '<span class="badge bg-warning">Voting</span>'; break;
        case 'passed': statusBadge = '<span class="badge bg-success">Passed</span>'; break;
        case 'rejected': statusBadge = '<span class="badge bg-danger">Rejected</span>'; break;
    }
    
    let votesSection = '';
    if (proposal.votes_summary) {
        votesSection = `
            <div class="card mb-3">
                <div class="card-header">Vote Results</div>
                <div class="card-body">
                    <p>Total Votes: ${proposal.votes_summary.total}</p>
                    <p>For: ${proposal.votes_summary.for_votes}</p>
                    <p>Against: ${proposal.votes_summary.against_votes}</p>
                    <p>Abstain: ${proposal.votes_summary.abstain_votes}</p>
                    <p>Absent: ${proposal.votes_summary.absent_votes}</p>
                    <p>Result: ${proposal.votes_summary.passed ? '<span class="badge bg-success">Passed</span>' : '<span class="badge bg-danger">Rejected</span>'}</p>
                </div>
            </div>
        `;
    }
    
    let actionButtons = '';
    if (proposal.status === 'draft' || proposal.status === 'submitted') {
        actionButtons = `
            <button class="btn btn-primary start-simulation" data-id="${proposal.id}">Start Simulation</button>
        `;
    }
    
    const content = `
        <div class="card">
            <div class="card-header d-flex justify-content-between">
                <h3>${proposal.title} ${statusBadge}</h3>
                <div>${actionButtons}</div>
            </div>
            <div class="card-body">
                <p><strong>Proposer:</strong> ${proposal.proposer.name} (${proposal.proposer.party.abbreviation})</p>
                <p><strong>Submitted:</strong> ${new Date(proposal.submitted_date).toLocaleString()}</p>
                ${proposal.vote_date ? `<p><strong>Vote Date:</strong> ${new Date(proposal.vote_date).toLocaleString()}</p>` : ''}
                <hr>
                <div class="proposal-content">
                    ${proposal.content}
                </div>
            </div>
        </div>
        
        ${votesSection}
    `;
    
    showDetail(content);
    
    // Add event listener for simulation button
    const simBtn = document.querySelector('.start-simulation');
    if (simBtn) {
        simBtn.addEventListener('click', async () => {
            const response = await postData(`/simulation/${proposal.id}/start`, {});
            if (response) {
                alert('Simulation started successfully! Check back later for results.');
                loadProposals();
            }
        });
    }
}

function showProposalForm() {
    const formHTML = `
        <div class="card">
            <div class="card-header">
                <h3>New Proposal</h3>
            </div>
            <div class="card-body">
                <form id="proposal-form">
                    <div class="mb-3">
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" required>
                    </div>
                    <div class="mb-3">
                        <label for="content" class="form-label">Content</label>
                        <textarea class="form-control" id="content" rows="5" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="proposer_id" class="form-label">Proposer ID</label>
                        <input type="number" class="form-control" id="proposer_id" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    `;
    
    showDetail(formHTML);
    
    // Add form submission handler
    document.getElementById('proposal-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const proposalData = {
            title: document.getElementById('title').value,
            content: document.getElementById('content').value,
            proposer_id: Number(document.getElementById('proposer_id').value)
        };
        
        const response = await postData('/proposals/', proposalData);
        if (response) {
            alert('Proposal created successfully!');
            loadProposals();
            showSection(proposalsContainer);
        }
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProposals();
});
