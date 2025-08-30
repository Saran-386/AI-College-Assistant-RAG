// Application State
let currentMode = 'qa';
let documents = [];
let chatHistory = [];

// Sample data from the provided JSON
const sampleData = {
    sampleDocuments: [
        {
            id: "doc1",
            name: "Computer Science Syllabus.pdf",
            type: "syllabus",
            content: "COMPUTER SCIENCE SYLLABUS\n\nUnit 1: Data Structures and Algorithms\n- Arrays and Linked Lists\n- Stacks and Queues\n- Trees and Graphs\n- Sorting and Searching Algorithms\n- Time and Space Complexity\n\nUnit 2: Internet of Things (IoT)\n- Introduction to IoT\n- Sensors and Actuators\n- Communication Protocols\n- IoT Architecture\n- Applications and Case Studies\n\nUnit 3: Cryptography and Network Security\n- Symmetric and Asymmetric Encryption\n- Hash Functions\n- Digital Signatures\n- Hill Cipher\n- RSA Algorithm\n- Network Security Protocols\n\nUnit 4: Database Management Systems\n- Relational Database Concepts\n- SQL Queries\n- Normalization\n- Transaction Management\n- Concurrency Control"
        }
    ],
    examQuestions: [
        {
            subject: "IoT",
            question: "Explain the architecture of IoT systems with a neat diagram.",
            marks: 16,
            type: "long_answer"
        },
        {
            subject: "Cryptography", 
            question: "Implement Hill Cipher encryption for the plaintext 'HELLO' using the key matrix [[3,2],[5,7]].",
            marks: 10,
            type: "numerical"
        },
        {
            subject: "Data Structures",
            question: "Write an algorithm for Binary Search Tree insertion and analyze its time complexity.",
            marks: 12,
            type: "algorithm"
        }
    ],
    studyNotes: {
        iot: "IoT (Internet of Things) connects physical devices to the internet, enabling data collection and remote control. Key components include sensors (temperature, humidity, motion), actuators (motors, LEDs), communication protocols (WiFi, Bluetooth, MQTT), and cloud platforms for data processing.",
        cryptography: "Hill Cipher is a polygraphic substitution cipher based on linear algebra. It uses matrix multiplication to encrypt blocks of plaintext. The key is an invertible matrix, and decryption requires the inverse matrix modulo 26.",
        dataStructures: "Binary Search Trees (BST) are hierarchical data structures where each node has at most two children. Left child contains values less than parent, right child contains greater values. This property enables efficient searching, insertion, and deletion operations."
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    initializeEventListeners();
    loadSampleDocument();
    updateUI();
});

// Event Listeners
function initializeEventListeners() {
    console.log('Initializing event listeners');
    
    // Get DOM elements
    const tabButtons = document.querySelectorAll('.tab-btn');
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const modeButtons = document.querySelectorAll('.mode-btn');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    console.log('Found tab buttons:', tabButtons.length);
    
    // Tab switching
    tabButtons.forEach(btn => {
        console.log('Adding event listener to tab:', btn.dataset.tab);
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('Tab clicked:', btn.dataset.tab);
            switchTab(btn.dataset.tab);
        });
    });

    // File upload
    if (uploadArea) {
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('drop', handleDrop);
        uploadArea.addEventListener('dragleave', handleDragLeave);
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }

    // Mode switching
    modeButtons.forEach(btn => {
        btn.addEventListener('click', () => switchMode(btn.dataset.mode));
    });

    // Chat input
    if (chatInput && sendBtn) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        sendBtn.addEventListener('click', sendMessage);
    }
}

// Tab Management
function switchTab(tabName) {
    console.log('Switching to tab:', tabName);
    
    const tabButtons = document.querySelectorAll('.tab-btn');
    const setupTab = document.getElementById('setup-tab');
    const assistantTab = document.getElementById('assistant-tab');
    
    // Update tab button states
    tabButtons.forEach(btn => {
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Show/hide tab content
    if (tabName === 'setup') {
        if (setupTab) {
            setupTab.classList.remove('hidden');
        }
        if (assistantTab) {
            assistantTab.classList.add('hidden');
        }
    } else if (tabName === 'assistant') {
        if (setupTab) {
            setupTab.classList.add('hidden');
        }
        if (assistantTab) {
            assistantTab.classList.remove('hidden');
        }
    }
    
    console.log('Tab switch completed');
}

function switchToAssistant() {
    console.log('Switch to assistant called');
    switchTab('assistant');
}

// File Upload Handlers
function handleDragOver(e) {
    e.preventDefault();
    const uploadArea = document.getElementById('upload-area');
    if (uploadArea) {
        uploadArea.classList.add('dragover');
    }
}

function handleDragLeave(e) {
    e.preventDefault();
    const uploadArea = document.getElementById('upload-area');
    if (uploadArea) {
        uploadArea.classList.remove('dragover');
    }
}

function handleDrop(e) {
    e.preventDefault();
    const uploadArea = document.getElementById('upload-area');
    if (uploadArea) {
        uploadArea.classList.remove('dragover');
    }
    const files = Array.from(e.dataTransfer.files);
    processFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    processFiles(files);
}

function processFiles(files) {
    const pdfFiles = files.filter(file => file.type === 'application/pdf');
    
    if (pdfFiles.length === 0) {
        showNotification('Please upload PDF files only.', 'error');
        return;
    }

    pdfFiles.forEach(file => {
        const document = {
            id: `doc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            name: file.name,
            type: detectDocumentType(file.name),
            content: generateMockContent(file.name),
            uploadedAt: new Date()
        };

        documents.push(document);
    });

    updateDocumentList();
    updateUI();
    showNotification(`${pdfFiles.length} document(s) uploaded successfully!`, 'success');
}

function detectDocumentType(filename) {
    const name = filename.toLowerCase();
    if (name.includes('syllabus')) return 'syllabus';
    if (name.includes('notes')) return 'notes';
    if (name.includes('exam') || name.includes('paper') || name.includes('question')) return 'exam';
    return 'document';
}

function generateMockContent(filename) {
    // Generate realistic content based on filename
    const name = filename.toLowerCase();
    if (name.includes('iot')) {
        return `IoT Study Material\n\n${sampleData.studyNotes.iot}\n\nTopics covered:\n- IoT Architecture\n- Sensor Networks\n- Communication Protocols\n- Cloud Integration\n- Security Considerations`;
    }
    if (name.includes('crypto')) {
        return `Cryptography Notes\n\n${sampleData.studyNotes.cryptography}\n\nKey Algorithms:\n- Caesar Cipher\n- Hill Cipher\n- RSA Encryption\n- Digital Signatures`;
    }
    if (name.includes('data') || name.includes('algorithm')) {
        return `Data Structures & Algorithms\n\n${sampleData.studyNotes.dataStructures}\n\nKey Topics:\n- Arrays and Lists\n- Trees and Graphs\n- Sorting Algorithms\n- Search Techniques`;
    }
    return `Study Material for ${filename}\n\nThis document contains comprehensive study material covering various computer science topics including algorithms, data structures, and software engineering principles.`;
}

// Document Management
function updateDocumentList() {
    const documentList = document.getElementById('document-list');
    const docCount = document.querySelector('.doc-count');
    
    if (!documentList) return;
    
    if (documents.length === 0) {
        documentList.innerHTML = '<p class="empty-state">No documents uploaded yet</p>';
    } else {
        documentList.innerHTML = documents.map(doc => `
            <div class="document-item">
                <div class="document-item__info">
                    <div class="document-item__name">${doc.name}</div>
                    <div class="document-item__type">${doc.type}</div>
                </div>
                <div class="document-item__actions">
                    <button onclick="viewDocument('${doc.id}')" title="View document">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="deleteDocument('${doc.id}')" class="delete-btn" title="Delete document">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    if (docCount) {
        docCount.textContent = `(${documents.length})`;
    }
}

function viewDocument(docId) {
    const doc = documents.find(d => d.id === docId);
    if (doc) {
        addMessage({
            type: 'system',
            content: `📄 **${doc.name}** (${doc.type})\n\n${doc.content.substring(0, 500)}${doc.content.length > 500 ? '...' : ''}`
        });
    }
}

function deleteDocument(docId) {
    documents = documents.filter(d => d.id !== docId);
    updateDocumentList();
    updateUI();
    showNotification('Document deleted successfully.', 'success');
}

// Mode Management
function switchMode(mode) {
    currentMode = mode;
    
    const modeButtons = document.querySelectorAll('.mode-btn');
    const modeTitle = document.getElementById('mode-title');
    const modeDescription = document.getElementById('mode-description');
    const chatInput = document.getElementById('chat-input');
    
    modeButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    const modeConfig = {
        qa: {
            title: 'General Q&A Mode',
            description: 'Ask questions about your uploaded documents'
        },
        exam: {
            title: 'Exam Prep Mode',
            description: 'Generate practice questions and MCQs'
        },
        summary: {
            title: 'Quick Summary Mode',
            description: 'Get concise summaries for quick revision'
        }
    };

    if (modeTitle) modeTitle.textContent = modeConfig[mode].title;
    if (modeDescription) modeDescription.textContent = modeConfig[mode].description;
    
    if (chatInput) {
        chatInput.placeholder = mode === 'summary' ? 'Request a summary...' : 
                               mode === 'exam' ? 'Ask for practice questions...' : 
                               'Ask a question...';
    }
}

// Chat Management
function addMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return null;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.type}`;
    
    if (message.type === 'loading') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
                <span>AI Assistant is thinking...</span>
            </div>
        `;
    } else {
        const icon = message.type === 'user' ? 'fa-user' : 'fa-robot';
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="fas ${icon}"></i>
                ${formatMessageContent(message.content)}
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
}

function formatMessageContent(content) {
    // Convert markdown-style formatting to HTML
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Convert newlines to paragraphs
    const paragraphs = formatted.split('\n\n').filter(p => p.trim());
    if (paragraphs.length > 1) {
        return paragraphs.map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
    } else {
        return `<p>${formatted.replace(/\n/g, '<br>')}</p>`;
    }
}

function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    if (!chatInput) return;
    
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage({
        type: 'user',
        content: message
    });

    // Clear input
    chatInput.value = '';

    // Show loading
    const loadingMessage = addMessage({
        type: 'loading',
        content: ''
    });

    // Generate AI response
    setTimeout(() => {
        if (loadingMessage) {
            loadingMessage.remove();
        }
        const aiResponse = generateAIResponse(message);
        addMessage({
            type: 'assistant',
            content: aiResponse
        });
    }, 1500 + Math.random() * 1000);
}

function generateAIResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    if (documents.length === 0) {
        return "I'd be happy to help! However, I notice you haven't uploaded any documents yet. Please upload some PDFs (syllabus, notes, or past papers) so I can provide more accurate and relevant answers.";
    }

    // Mode-specific responses
    if (currentMode === 'summary') {
        return generateSummaryResponse(message);
    } else if (currentMode === 'exam') {
        return generateExamResponse(message);
    } else {
        return generateQAResponse(message);
    }
}

function generateQAResponse(message) {
    // IoT related questions
    if (message.includes('iot') || message.includes('internet of things')) {
        if (message.includes('unit 2') || message.includes('topics')) {
            return `Based on your uploaded syllabus, **Unit 2: Internet of Things (IoT)** covers the following topics:

• **Introduction to IoT** - Basic concepts and definitions
• **Sensors and Actuators** - Hardware components for data collection and control
• **Communication Protocols** - WiFi, Bluetooth, MQTT, CoAP
• **IoT Architecture** - Device, connectivity, data processing, and application layers
• **Applications and Case Studies** - Smart homes, industrial IoT, healthcare applications

${sampleData.studyNotes.iot}`;
        }
        return `IoT (Internet of Things) is a network of interconnected devices that can collect and exchange data. Key components include sensors for data collection, actuators for control, communication protocols for connectivity, and cloud platforms for data processing and analytics.`;
    }

    // Cryptography related questions
    if (message.includes('cryptography') || message.includes('hill cipher') || message.includes('encryption')) {
        if (message.includes('hill cipher')) {
            return `**Hill Cipher** is a polygraphic substitution cipher that encrypts multiple characters at once using matrix multiplication.

**How it works:**
1. Convert plaintext to numbers (A=0, B=1, ..., Z=25)
2. Arrange in vectors of size n (key matrix size)
3. Multiply by the key matrix modulo 26
4. Convert back to letters

**Example:** For plaintext 'HELLO' with key matrix [[3,2],[5,7]]
- HE → [7,4] × [[3,2],[5,7]] = [37,42] ≡ [11,16] (mod 26) → LP
- LL → [11,11] × [[3,2],[5,7]] = [88,99] ≡ [10,21] (mod 26) → KV
- O → Add padding, then encrypt

**Advantages:** Resistant to frequency analysis
**Disadvantages:** Vulnerable if key matrix is known or guessed`;
        }
        return `Based on your uploaded content, cryptography covers symmetric/asymmetric encryption, hash functions, digital signatures, and specific algorithms like Hill Cipher and RSA. ${sampleData.studyNotes.cryptography}`;
    }

    // Data structures related questions
    if (message.includes('data structure') || message.includes('algorithm') || message.includes('tree') || message.includes('bst')) {
        if (message.includes('bst') || message.includes('binary search tree')) {
            return `**Binary Search Tree (BST) Properties:**

**Structure:** Each node has at most two children
• Left subtree contains values less than the parent
• Right subtree contains values greater than the parent

**Insertion Algorithm:**
\`\`\`
function insert(root, value):
    if root is null:
        return new Node(value)
    
    if value < root.data:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    
    return root
\`\`\`

**Time Complexity Analysis:**
• **Best/Average Case:** O(log n) - balanced tree
• **Worst Case:** O(n) - skewed tree (becomes like a linked list)
• **Space Complexity:** O(log n) for recursive calls

**Applications:** Efficient searching, sorting, and range queries`;
        }
        return `Data Structures and Algorithms form the foundation of computer science. Key topics include arrays, linked lists, stacks, queues, trees, graphs, and various sorting/searching algorithms. ${sampleData.studyNotes.dataStructures}`;
    }

    // Database related questions
    if (message.includes('database') || message.includes('sql') || message.includes('dbms')) {
        return `**Database Management Systems (Unit 4)** covers:

• **Relational Database Concepts** - Tables, relationships, keys
• **SQL Queries** - SELECT, INSERT, UPDATE, DELETE operations
• **Normalization** - 1NF, 2NF, 3NF, BCNF to eliminate redundancy
• **Transaction Management** - ACID properties, concurrency control
• **Concurrency Control** - Locking mechanisms, deadlock prevention

Would you like me to elaborate on any specific database concept?`;
    }

    // General syllabus questions
    if (message.includes('unit') || message.includes('syllabus') || message.includes('topics')) {
        return `Based on your uploaded **Computer Science Syllabus**, here are the main units:

**Unit 1: Data Structures and Algorithms**
- Arrays, Linked Lists, Stacks, Queues
- Trees, Graphs, Sorting & Searching
- Time & Space Complexity

**Unit 2: Internet of Things (IoT)**
- IoT Introduction, Sensors & Actuators
- Communication Protocols, Architecture
- Applications & Case Studies

**Unit 3: Cryptography and Network Security**
- Symmetric/Asymmetric Encryption
- Hash Functions, Digital Signatures
- Hill Cipher, RSA Algorithm

**Unit 4: Database Management Systems**
- Relational Concepts, SQL Queries
- Normalization, Transaction Management

Which unit would you like to explore in more detail?`;
    }

    // Default response
    return `I understand you're asking about "${userMessage}". Based on your uploaded documents, I can help explain concepts related to data structures, IoT, cryptography, and databases. Could you be more specific about which topic you'd like to explore? For example:

• "Explain IoT architecture"
• "How does Hill Cipher work?"
• "What is a Binary Search Tree?"
• "What are the topics in Unit 2?"`;
}

function generateExamResponse(message) {
    const examQuestions = [
        "**16-mark IoT Question:**\nExplain the architecture of IoT systems with a neat diagram. Discuss the role of sensors, actuators, and communication protocols in IoT implementation.",
        
        "**10-mark Cryptography Question:**\nImplement Hill Cipher encryption for the plaintext 'HELLO' using the key matrix [[3,2],[5,7]]. Show all calculation steps.",
        
        "**12-mark Data Structures Question:**\nWrite an algorithm for Binary Search Tree insertion and analyze its time complexity. Provide examples for best and worst-case scenarios.",
        
        "**MCQ Practice:**\n1. Which of the following is NOT a property of BST?\na) Left child < parent\nb) Right child > parent\nc) All nodes have exactly 2 children ✓\nd) Inorder traversal gives sorted sequence",
        
        "**Short Answer (5 marks):**\nList and briefly explain the four main layers of IoT architecture.",
        
        "**Numerical Problem (8 marks):**\nCalculate the time complexity of searching in a balanced BST with 1000 nodes. Justify your answer."
    ];
    
    return `Here are some practice questions based on your uploaded content:

${examQuestions[Math.floor(Math.random() * examQuestions.length)]}

**Study Tips for Exam Prep:**
• Focus on understanding core concepts rather than memorization
• Practice numerical problems and algorithm implementations
• Draw diagrams for architectural questions
• Review past year questions for pattern recognition

Would you like more questions from a specific topic?`;
}

function generateSummaryResponse(message) {
    if (message.includes('unit 2') || message.includes('iot')) {
        return `**📋 Unit 2: IoT - Quick Summary**

**🔑 Key Points:**
1. **IoT Definition:** Network of connected devices collecting and sharing data
2. **Core Components:** Sensors (input), Actuators (output), Communication protocols
3. **Architecture Layers:** Device → Connectivity → Data Processing → Application
4. **Protocols:** WiFi, Bluetooth, MQTT, CoAP for device communication
5. **Applications:** Smart homes, Industrial IoT, Healthcare monitoring

**💡 Remember:** IoT = Things + Internet + Data Analytics`;
    }
    
    if (message.includes('unit 3') || message.includes('cryptography')) {
        return `**📋 Unit 3: Cryptography - Quick Summary**

**🔑 Key Points:**
1. **Symmetric Encryption:** Same key for encryption/decryption (faster)
2. **Asymmetric Encryption:** Public-private key pairs (secure)
3. **Hash Functions:** One-way functions for data integrity
4. **Hill Cipher:** Matrix-based polygraphic cipher
5. **Digital Signatures:** Authentication and non-repudiation

**💡 Remember:** Security = Confidentiality + Integrity + Authentication`;
    }

    if (message.includes('syllabus') || message.includes('all units')) {
        return `**📋 Complete CS Syllabus - Quick Summary**

**Unit 1 - Data Structures & Algorithms:**
Arrays, Lists, Trees, Graphs, Sorting, Searching, Complexity Analysis

**Unit 2 - Internet of Things:**
IoT Architecture, Sensors, Communication Protocols, Applications

**Unit 3 - Cryptography & Security:**
Encryption Methods, Hash Functions, Digital Signatures, Ciphers

**Unit 4 - Database Management:**
Relational Model, SQL, Normalization, Transactions, Concurrency

**🎯 Focus Areas:** Practical implementation + theoretical understanding`;
    }

    return `**📋 Study Material Summary**

Based on your uploaded documents, here's a concise overview:

**🔍 Main Topics Covered:**
• Data Structures and Algorithms
• Internet of Things (IoT)
• Cryptography and Security
• Database Management

**📚 Study Strategy:**
1. Understand core concepts first
2. Practice implementation problems
3. Review real-world applications
4. Solve previous year questions

**⏰ Quick Revision Tips:**
• Make concept maps
• Practice coding problems
• Memorize key formulas
• Review case studies

What specific topic would you like me to summarize in more detail?`;
}

// UI Update Functions
function updateUI() {
    const hasDocuments = documents.length > 0;
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (chatInput) {
        chatInput.disabled = !hasDocuments;
        if (hasDocuments) {
            chatInput.placeholder = currentMode === 'summary' ? 'Request a summary...' : 
                                   currentMode === 'exam' ? 'Ask for practice questions...' : 
                                   'Ask a question...';
        } else {
            chatInput.placeholder = 'Upload documents first...';
        }
    }
    
    if (sendBtn) {
        sendBtn.disabled = !hasDocuments;
    }
}

// Load sample document for demo
function loadSampleDocument() {
    const sampleDoc = {
        id: sampleData.sampleDocuments[0].id,
        name: sampleData.sampleDocuments[0].name,
        type: sampleData.sampleDocuments[0].type,
        content: sampleData.sampleDocuments[0].content,
        uploadedAt: new Date()
    };
    
    documents.push(sampleDoc);
    updateDocumentList();
    updateUI();
    
    // Add a welcome message
    setTimeout(() => {
        addMessage({
            type: 'assistant',
            content: `Welcome! I've loaded a sample **Computer Science Syllabus** to get you started. You can now:

• Ask questions about the syllabus content
• Switch to **Exam Prep Mode** for practice questions  
• Use **Summary Mode** for quick revision notes
• Upload additional documents (notes, past papers)

Try asking: *"What topics are in Unit 2?"* or *"Explain Hill Cipher"*`
        });
    }, 1000);
}

// Utility Functions
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    if (!notification) return;
    
    const notificationIcon = notification.querySelector('.notification-icon');
    const notificationMessage = notification.querySelector('.notification-message');
    
    notification.className = `notification ${type}`;
    if (notificationIcon) {
        notificationIcon.className = `notification-icon fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}`;
    }
    if (notificationMessage) {
        notificationMessage.textContent = message;
    }
    
    notification.classList.remove('hidden');
    setTimeout(() => notification.classList.add('show'), 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.classList.add('hidden'), 300);
    }, 3000);
}

// Export functions for global access
window.switchToAssistant = switchToAssistant;
window.viewDocument = viewDocument;
window.deleteDocument = deleteDocument;