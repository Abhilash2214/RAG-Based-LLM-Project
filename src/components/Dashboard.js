import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import {
  FaUser,
  FaSignOutAlt,
  FaHome,
  FaFileUpload,
  FaChartBar,
  FaCog,
  FaBell,
  FaSearch,
  FaCloudUploadAlt,
  FaQuestionCircle,
  FaRobot,
  FaBookOpen,
  FaPlus,
  FaDownload,
  FaEye,
  FaTrash,
  FaArrowLeft
} from 'react-icons/fa';

const Dashboard = () => {
  const { currentUser, userProfile, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const uploadInputRef = useRef(null);
  const [userLibrary, setUserLibrary] = useState([]);
  const [libraryLoading, setLibraryLoading] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [isAsking, setIsAsking] = useState(false);
  const [qaHistory, setQaHistory] = useState([]);
  const [realTimeStats, setRealTimeStats] = useState({
    totalDocuments: 0,
    totalQuestions: 0,
    totalResponses: 0,
    storageUsed: '0 MB',
    documentsChange: '+0%',
    questionsChange: '+0%',
    responsesChange: '+0%',
    storageChange: '+0%'
  });
  const [ragStats, setRagStats] = useState({
    documents_in_rag: 0,
    total_chunks: 0,
    vector_dimension: 384,
    embedding_model: 'sentence-transformers/all-MiniLM-L6-v2',
    retrieval_method: 'FAISS Vector Search',
    rag_enabled: true,
    system_status: 'loading'
  });
  const [uploadedFiles] = useState([
    {
      id: 1,
      name: 'Research_Paper_2024.pdf',
      size: '2.4 MB',
      uploadDate: '2024-03-15',
      status: 'processed',
      questions: 15,
      type: 'pdf'
    },
    {
      id: 2,
      name: 'Business_Report.pdf',
      size: '1.8 MB',
      uploadDate: '2024-03-14',
      status: 'processing',
      questions: 8,
      type: 'pdf'
    },
    {
      id: 3,
      name: 'Documentation.pdf',
      size: '3.2 MB',
      uploadDate: '2024-03-13',
      status: 'processed',
      questions: 22,
      type: 'pdf'
    }
  ]);

  const [recentQuestions] = useState([
    {
      id: 1,
      question: "What are the main findings in the research paper?",
      document: "Research_Paper_2024.pdf",
      timestamp: "2 hours ago",
      answered: true
    },
    {
      id: 2,
      question: "Can you summarize the business metrics mentioned?",
      document: "Business_Report.pdf",
      timestamp: "5 hours ago",
      answered: true
    },
    {
      id: 3,
      question: "What are the installation requirements?",
      document: "Documentation.pdf",
      timestamp: "1 day ago",
      answered: true
    }
  ]);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };



  const sidebarItems = [
    { id: 'overview', label: 'Overview', icon: FaHome },
    { id: 'upload', label: 'Upload Documents', icon: FaFileUpload },
    { id: 'library', label: 'Books Library', icon: FaBookOpen },
    { id: 'qa', label: 'Q&A Chat', icon: FaQuestionCircle },
    { id: 'analytics', label: 'Analytics', icon: FaChartBar },
    { id: 'settings', label: 'Settings', icon: FaCog },
  ];

  const stats = [
    {
      label: 'Documents Processed',
      value: realTimeStats.totalDocuments.toString(),
      change: realTimeStats.documentsChange,
      icon: FaBookOpen,
      color: 'from-blue-500 to-blue-600'
    },
    {
      label: 'RAG-Enhanced Docs',
      value: (realTimeStats.ragDocuments || 0).toString(),
      change: `${realTimeStats.ragAdoptionRate || 0}% adoption`,
      icon: FaRobot,
      color: 'from-emerald-500 to-emerald-600'
    },
    {
      label: 'Questions Asked',
      value: realTimeStats.totalQuestions.toString(),
      change: realTimeStats.questionsChange,
      icon: FaQuestionCircle,
      color: 'from-green-500 to-green-600'
    },
    {
      label: 'Vector Chunks',
      value: ragStats.total_chunks.toString(),
      change: ragStats.system_status === 'operational' ? '✓ Active' : '⚠ Issues',
      icon: FaSearch,
      color: 'from-purple-500 to-purple-600'
    }
  ];

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={stat.label}
            className={`glass-morphism rounded-2xl p-6 card-hover animate-slide-up animation-delay-${index * 200}`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.color} flex items-center justify-center`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <span className="text-green-400 text-sm font-semibold">{stat.change}</span>
            </div>
            <h3 className="text-2xl font-bold text-white mb-1">{stat.value}</h3>
            <p className="text-gray-400 text-sm">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* RAG System Status */}
      <div className="glass-morphism rounded-2xl p-6 mb-6">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center">
          <FaRobot className="mr-3 text-primary-400" />
          RAG System Status
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-dark-800/50 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400 text-sm">Vector Store</span>
              <div className={`w-3 h-3 rounded-full ${ragStats.system_status === 'operational' ? 'bg-green-400' : 'bg-red-400'}`}></div>
            </div>
            <p className="text-white font-bold">{ragStats.retrieval_method}</p>
            <p className="text-gray-500 text-xs">{ragStats.total_chunks} chunks indexed</p>
          </div>
          
          <div className="bg-dark-800/50 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400 text-sm">Embedding Model</span>
              <span className="text-green-400 text-xs">✓ Active</span>
            </div>
            <p className="text-white font-bold text-sm">SentenceTransformers</p>
            <p className="text-gray-500 text-xs">{ragStats.vector_dimension}D embeddings</p>
          </div>
          
          <div className="bg-dark-800/50 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400 text-sm">System Health</span>
              <span className={`text-xs ${
                realTimeStats.systemHealth === 'excellent' ? 'text-green-400' : 
                realTimeStats.systemHealth === 'good' ? 'text-yellow-400' : 'text-red-400'
              }`}>
                {realTimeStats.systemHealth?.toUpperCase() || 'UNKNOWN'}
              </span>
            </div>
            <p className="text-white font-bold">{realTimeStats.ragAdoptionRate || 0}% Adoption</p>
            <p className="text-gray-500 text-xs">RAG-enhanced documents</p>
          </div>
        </div>
        
        <div className="mt-4 p-4 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl border border-blue-500/20">
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <FaRobot className="w-4 h-4 text-blue-400" />
            </div>
            <div>
              <h4 className="text-white font-semibold text-sm mb-1">RAG Enhancement Active</h4>
              <p className="text-gray-300 text-xs leading-relaxed">
                Your documents are being processed with advanced Retrieval-Augmented Generation technology, 
                enabling more accurate and contextual responses to your questions through vector similarity search.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Recent Documents */}
        <div className="glass-morphism rounded-2xl p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <FaBookOpen className="mr-3 text-primary-400" />
            Recent Documents
          </h3>
          <div className="space-y-3">
            {uploadedFiles.slice(0, 3).map((file) => (
              <div key={file.id} className="flex items-center justify-between p-3 bg-dark-800/50 rounded-xl hover:bg-dark-700/50 transition-colors">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
                    <FaBookOpen className="w-5 h-5 text-red-400" />
                  </div>
                  <div>
                    <p className="text-white font-medium text-sm">{file.name}</p>
                    <p className="text-gray-400 text-xs">{file.size} • {file.uploadDate}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    file.status === 'processed' 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {file.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Q&A */}
        <div className="glass-morphism rounded-2xl p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <FaQuestionCircle className="mr-3 text-accent-400" />
            Recent Questions
          </h3>
          <div className="space-y-3">
            {recentQuestions.map((qa) => (
              <div key={qa.id} className="p-3 bg-dark-800/50 rounded-xl hover:bg-dark-700/50 transition-colors">
                <p className="text-white text-sm mb-2 line-clamp-2">{qa.question}</p>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-400">{qa.document}</span>
                  <span className="text-gray-500">{qa.timestamp}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderUpload = () => (
    <div className="space-y-6">
      {/* Upload Area */}
      <div className="glass-morphism rounded-2xl p-8">
        <div
          className="border-2 border-dashed border-gray-600 rounded-xl p-12 text-center hover:border-primary-400 transition-colors"
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const files = Array.from(e.dataTransfer.files);
            if (files.length > 0) {
              setSelectedFiles(files);
              uploadToLibrary(files);
            }
          }}
        >
          <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce-slow">
            <FaCloudUploadAlt className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-2xl font-semibold text-white mb-2">Upload Your Documents</h3>
          <p className="text-gray-400 mb-6">Drag and drop your PDF files here, or click to browse</p>
          <input
            type="file"
            multiple
            accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.gif,.xls,.xlsx,.csv"
            ref={uploadInputRef}
            onChange={(e) => {
              const files = Array.from(e.target.files);
              if (files.length > 0) {
                setSelectedFiles(files);
                uploadToLibrary(files);
              }
              e.target.value = ''; // allow re-selecting the same file
            }}
            className="hidden"
          />
          <button
            type="button"
            className="btn-primary"
            onClick={() => uploadInputRef.current?.click()}
            disabled={uploading}
          >
            <FaPlus className="mr-2" />
            Choose Files
          </button>
        </div>
      </div>

      {/* Uploaded Files List */}
      <div className="glass-morphism rounded-2xl p-6">
        <h3 className="text-xl font-bold text-white mb-4">Your Documents ({userLibrary.length})</h3>
        {libraryLoading ? (
          <p className="text-gray-400">Loading your documents...</p>
        ) : userLibrary.length === 0 ? (
          <p className="text-gray-400">No documents yet. Upload your first document!</p>
        ) : (
          <div className="space-y-3">
            {userLibrary.map((doc) => (
              <div key={doc.document_id} className="flex items-center justify-between p-4 bg-dark-800/50 rounded-xl hover:bg-dark-700/50 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-red-500/20 rounded-xl flex items-center justify-center">
                    <FaBookOpen className="w-6 h-6 text-red-400" />
                  </div>
                  <div>
                    <h4 className="text-white font-medium">{doc.original_filename}</h4>
                    <p className="text-gray-400 text-sm">
                      {(doc.file_size / 1024 / 1024).toFixed(2)} MB • {new Date(doc.upload_timestamp).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    doc.metadata?.processing_status === 'completed' || doc.metadata?.processing_status === 'error_with_fallback'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {doc.metadata?.processing_status === 'error_with_fallback'
                      ? 'processed'
                      : doc.metadata?.processing_status || 'processing'}
                  </span>
                  <div className="flex space-x-2">
                    <button
                      type="button"
                      onClick={() => viewDocument(doc)}
                      className="text-gray-400 hover:text-primary-400 transition-colors"
                      title="View"
                    >
                      <FaEye className="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      onClick={() => downloadDocument(doc)}
                      className="text-gray-400 hover:text-green-400 transition-colors"
                      title="Download"
                    >
                      <FaDownload className="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      onClick={() => confirmDeleteDocument(doc)}
                      className="text-gray-400 hover:text-red-400 transition-colors"
                      title="Delete"
                    >
                      <FaTrash className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  // API Functions
  const uploadToLibrary = async (files) => {
    if (!currentUser) return;
    
    setUploading(true);
    const results = [];
    
    for (const file of files) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', currentUser.uid);
        
        const response = await fetch('http://localhost:5000/api/upload', {
          method: 'POST',
          body: formData,
        });
        
        if (response.ok) {
          const result = await response.json();
          results.push({ success: true, filename: file.name, result });
        } else {
          results.push({ success: false, filename: file.name, error: 'Upload failed' });
        }
      } catch (error) {
        results.push({ success: false, filename: file.name, error: error.message });
      }
    }
    
    setUploading(false);
    await fetchUserLibrary(); // Refresh library
    return results;
  };

  const fetchUserLibrary = useCallback(async () => {
    if (!currentUser) return;
    
    setLibraryLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/library/${currentUser.uid}`);
      if (response.ok) {
        const library = await response.json();
        setUserLibrary(library.documents || []);
      }
    } catch (error) {
      console.error('Error fetching library:', error);
    }
    setLibraryLoading(false);
  }, [currentUser]);

  const deleteDocument = async (documentId) => {
    if (!currentUser) return;
    
    try {
      const response = await fetch(`http://localhost:5000/api/delete/${currentUser.uid}/${documentId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        await fetchUserLibrary(); // Refresh library
        return true;
      }
    } catch (error) {
      console.error('Error deleting document:', error);
    }
    return false;
  };

  const viewDocument = (doc) => {
    if (!currentUser) return;
    window.open(
      `http://localhost:5000/api/file/${currentUser.uid}/${doc.document_id}`,
      '_blank'
    );
  };

  const downloadDocument = (doc) => {
    if (!currentUser) return;
    const a = document.createElement('a');
    a.href = `http://localhost:5000/api/file/${currentUser.uid}/${doc.document_id}?download=1`;
    a.download = doc.original_filename || 'document';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const confirmDeleteDocument = async (doc) => {
    if (window.confirm(`Delete "${doc.original_filename}"? This cannot be undone.`)) {
      await deleteDocument(doc.document_id);
    }
  };

  // Q&A Functions
  const selectDocumentForQA = async (document) => {
    setSelectedDocument(document);
    setChatMessages([
      {
        type: 'system',
        message: `Selected "${document.original_filename}" for Q&A. You can now ask questions about this document.`,
        timestamp: new Date().toISOString()
      }
    ]);
    setActiveTab('qa');
  };

  const askQuestion = async (question) => {
    if (!selectedDocument || !question.trim()) return;
    
    setIsAsking(true);
    
    // Add user question to chat
    const userMessage = {
      type: 'user',
      message: question,
      timestamp: new Date().toISOString()
    };
    
    setChatMessages(prev => [...prev, userMessage]);
    setCurrentQuestion('');
    
    try {
      const response = await fetch('http://localhost:5000/api/qa/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: currentUser.uid,
          document_id: selectedDocument.document_id,
          question: question.trim()
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        
        // Add AI response to chat with RAG metadata
        const aiMessage = {
          type: 'ai',
          message: result.answer,
          timestamp: result.timestamp,
          document: selectedDocument.original_filename,
          ragMetadata: result.rag_metadata,
          questionType: result.question_type
        };
        
        setChatMessages(prev => [...prev, aiMessage]);
      } else {
        const error = await response.json();
        setChatMessages(prev => [...prev, {
          type: 'error',
          message: error.error || 'Failed to get answer',
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (error) {
      setChatMessages(prev => [...prev, {
        type: 'error',
        message: 'Network error occurred',
        timestamp: new Date().toISOString()
      }]);
    }
    
    setIsAsking(false);
  };

  const fetchQAHistory = useCallback(async () => {
    if (!currentUser) return;
    
    try {
      const response = await fetch(`http://localhost:5000/api/qa/history/${currentUser.uid}`);
      if (response.ok) {
        const history = await response.json();
        setQaHistory(history.recent_sessions || []);
        return history;
      }
    } catch (error) {
      console.error('Error fetching Q&A history:', error);
    }
    return null;
  }, [currentUser]);

  const fetchRagStats = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5000/api/rag/stats');
      if (response.ok) {
        const stats = await response.json();
        setRagStats(stats);
      }
    } catch (error) {
      console.error('Error fetching RAG stats:', error);
      setRagStats(prev => ({ ...prev, system_status: 'error' }));
    }
  }, []);

  const fetchIndividualStats = useCallback(async () => {
    try {
      // Fetch library data
      const libraryResponse = await fetch(`http://localhost:5000/api/library/${currentUser.uid}`);
      let totalDocuments = 0;
      let totalStorage = 0;
      let processedDocuments = 0;
      let ragDocuments = 0;
      
      if (libraryResponse.ok) {
        const library = await libraryResponse.json();
        totalDocuments = library.total_documents || 0;
        
        // Calculate storage used and RAG documents
        if (library.documents) {
          totalStorage = library.documents.reduce((sum, doc) => sum + (doc.file_size || 0), 0);
          processedDocuments = library.documents.filter(doc => 
            doc.metadata?.processing_status === 'completed' || 
            doc.metadata?.has_gemini_analysis
          ).length;
          ragDocuments = library.documents.filter(doc => doc.rag_processed).length;
        }
      }
      
      // Fetch Q&A history
      const qaResponse = await fetch(`http://localhost:5000/api/qa/history/${currentUser.uid}`);
      let totalQuestions = 0;
      let totalResponses = 0;
      
      if (qaResponse.ok) {
        const qaHistory = await qaResponse.json();
        totalQuestions = qaHistory.total_sessions || 0;
        totalResponses = totalQuestions; // Each question has a response
      }
      
      // Calculate storage in MB
      const storageInMB = (totalStorage / (1024 * 1024)).toFixed(1);
      const ragAdoptionRate = totalDocuments > 0 ? (ragDocuments / totalDocuments * 100).toFixed(1) : 0;
      
      setRealTimeStats({
        totalDocuments,
        totalQuestions,
        totalResponses,
        ragDocuments,
        ragAdoptionRate,
        storageUsed: `${storageInMB} MB`,
        documentsChange: totalDocuments > 0 ? '+12%' : '+0%',
        questionsChange: totalQuestions > 0 ? '+23%' : '+0%',
        responsesChange: totalResponses > 0 ? '+18%' : '+0%',
        storageChange: totalStorage > 0 ? '+5%' : '+0%',
        processedDocuments,
        systemHealth: ragAdoptionRate > 80 ? 'excellent' : ragAdoptionRate > 50 ? 'good' : 'fair'
      });
      
    } catch (error) {
      console.error('Error fetching individual stats:', error);
    }
  }, [currentUser]);

  const fetchRealTimeStats = useCallback(async () => {
    if (!currentUser) return;
    
    try {
      // Fetch from new real-time stats endpoint
      const statsResponse = await fetch('http://localhost:5000/api/real-time-stats');
      if (statsResponse.ok) {
        const stats = await statsResponse.json();
        setRealTimeStats({
          totalDocuments: stats.total_documents,
          totalQuestions: stats.total_questions,
          totalResponses: stats.total_questions,
          ragDocuments: stats.rag_documents,
          ragAdoptionRate: stats.rag_adoption_rate,
          storageUsed: `${(stats.total_documents * 0.5).toFixed(1)} MB`, // Estimate
          documentsChange: stats.total_documents > 0 ? '+12%' : '+0%',
          questionsChange: stats.total_questions > 0 ? '+23%' : '+0%',
          responsesChange: stats.total_questions > 0 ? '+18%' : '+0%',
          storageChange: stats.total_documents > 0 ? '+5%' : '+0%',
          systemHealth: stats.system_health,
          totalUsers: stats.total_users,
          documentsPerUser: stats.documents_per_user,
          questionsPerDocument: stats.questions_per_document
        });
      } else {
        // Fallback to individual API calls
        await fetchIndividualStats();
      }
      
    } catch (error) {
      console.error('Error fetching real-time stats:', error);
      await fetchIndividualStats();
    }
  }, [currentUser, fetchIndividualStats]);

  // Load data when user changes or component mounts
  useEffect(() => {
    if (currentUser) {
      fetchUserLibrary();
      fetchQAHistory();
      fetchRealTimeStats();
      fetchRagStats();
    }
  }, [currentUser, fetchUserLibrary, fetchQAHistory, fetchRealTimeStats, fetchRagStats]);

  // Render Functions
  const renderLibrary = () => (
    <div className="space-y-6">
      {/* Library Header */}
      <div className="glass-morphism rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">Books Library</h2>
            <p className="text-gray-400">Upload and manage your documents with AI-powered processing</p>
          </div>
          <button
            onClick={fetchUserLibrary}
            className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-xl transition-colors flex items-center space-x-2"
          >
            <FaEye className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>

        {/* File Upload Area */}
        <div className="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-primary-500 transition-colors">
          <FaCloudUploadAlt className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">Upload Documents</h3>
          <p className="text-gray-400 mb-4">
            Drag and drop files here, or click to select files
          </p>
          <input
            type="file"
            multiple
            accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.gif,.xls,.xlsx,.csv"
            onChange={(e) => {
              const files = Array.from(e.target.files);
              setSelectedFiles(files);
              if (files.length > 0) {
                uploadToLibrary(files);
              }
            }}
            className="hidden"
            id="library-file-upload"
          />
          <label
            htmlFor="library-file-upload"
            className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold rounded-xl hover:from-primary-600 hover:to-accent-600 transition-all duration-300 cursor-pointer"
          >
            <FaPlus className="w-4 h-4 mr-2" />
            Choose Files
          </label>
          <p className="text-xs text-gray-500 mt-2">
            Supported: PDF, DOC, DOCX, TXT, Images, Excel files (Max 10MB each)
          </p>
        </div>

        {/* Upload Progress */}
        {uploading && (
          <div className="mt-4 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl">
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-500"></div>
              <span className="text-blue-400">Processing files with AI...</span>
            </div>
          </div>
        )}
      </div>

      {/* Library Content */}
      <div className="glass-morphism rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white">Your Documents ({userLibrary.length})</h3>
          <div className="flex items-center space-x-3">
            <div className="relative">
              <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search library..."
                className="pl-10 pr-4 py-2 bg-dark-800/50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 w-64"
              />
            </div>
          </div>
        </div>

        {libraryLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading your library...</p>
          </div>
        ) : userLibrary.length === 0 ? (
          <div className="text-center py-8">
            <FaBookOpen className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <h4 className="text-lg font-semibold text-white mb-2">No documents yet</h4>
            <p className="text-gray-400">Upload your first document to get started!</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {userLibrary.map((doc) => (
              <div
                key={doc.document_id}
                className="flex items-center justify-between p-4 bg-dark-800/50 rounded-xl hover:bg-dark-700/50 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                    {doc.file_type?.startsWith('image/') ? (
                      <FaEye className="w-6 h-6 text-white" />
                    ) : (
                      <FaBookOpen className="w-6 h-6 text-white" />
                    )}
                  </div>
                  <div>
                    <h4 className="text-white font-medium">{doc.original_filename}</h4>
                    <div className="flex items-center space-x-4 text-sm text-gray-400">
                      <span>{(doc.file_size / 1024 / 1024).toFixed(2)} MB</span>
                      <span>{new Date(doc.upload_timestamp).toLocaleDateString()}</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        doc.metadata?.processing_status === 'completed'
                          ? 'bg-green-500/20 text-green-400'
                          : doc.metadata?.processing_status === 'error_with_fallback'
                          ? 'bg-yellow-500/20 text-yellow-400'
                          : doc.metadata?.has_gemini_analysis
                          ? 'bg-blue-500/20 text-blue-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}>
                        {doc.metadata?.processing_status === 'error_with_fallback' 
                          ? 'processed' 
                          : doc.metadata?.processing_status || 'unknown'}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => selectDocumentForQA(doc)}
                    className="p-2 text-green-400 hover:text-green-300 hover:bg-green-500/10 rounded-lg transition-colors"
                    title="Start Q&A Chat"
                  >
                    <FaQuestionCircle className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => viewDocument(doc)}
                    className="p-2 text-blue-400 hover:text-blue-300 hover:bg-blue-500/10 rounded-lg transition-colors"
                    title="View Details"
                  >
                    <FaEye className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => confirmDeleteDocument(doc)}
                    className="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <FaTrash className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderQA = () => (
    <div className="space-y-6">
      {/* Q&A Header */}
      <div className="glass-morphism rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">Q&A Chat</h2>
            <p className="text-gray-400">Ask questions about your documents using AI</p>
          </div>
          <button
            onClick={fetchQAHistory}
            className="px-4 py-2 bg-accent-500 hover:bg-accent-600 text-white rounded-xl transition-colors flex items-center space-x-2"
          >
            <FaQuestionCircle className="w-4 h-4" />
            <span>History</span>
          </button>
        </div>

        {/* Document Selection */}
        {!selectedDocument ? (
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Select a Document</h3>
            <div className="grid gap-3 max-h-96 overflow-y-auto">
              {userLibrary.length === 0 ? (
                <div className="text-center py-8">
                  <FaBookOpen className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">No documents available. Upload some documents first!</p>
                </div>
              ) : (
                userLibrary.map((doc) => (
                  <div
                    key={doc.document_id}
                    onClick={() => selectDocumentForQA(doc)}
                    className="flex items-center justify-between p-4 bg-dark-800/50 rounded-xl hover:bg-primary-500/20 cursor-pointer transition-colors border border-transparent hover:border-primary-500/30"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                        {doc.file_type?.startsWith('image/') ? (
                          <FaEye className="w-5 h-5 text-white" />
                        ) : (
                          <FaBookOpen className="w-5 h-5 text-white" />
                        )}
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <h4 className="text-white font-medium">{doc.original_filename}</h4>
                          {doc.rag_processed && (
                            <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 text-xs rounded-full border border-emerald-500/30">
                              RAG
                            </span>
                          )}
                        </div>
                        <p className="text-gray-400 text-sm">
                          {(doc.file_size / 1024 / 1024).toFixed(2)} MB • {new Date(doc.upload_timestamp).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="text-primary-400">
                      <FaQuestionCircle className="w-5 h-5" />
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        ) : (
          /* Chat Interface */
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => {
                    setSelectedDocument(null);
                    setChatMessages([]);
                  }}
                  className="px-4 py-2 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-500 hover:to-gray-600 text-white rounded-xl transition-all duration-300 flex items-center space-x-2 font-medium"
                >
                  <FaArrowLeft className="w-4 h-4" />
                  <span>Back to Documents</span>
                </button>
                <div className="h-6 w-px bg-gray-600"></div>
                <h3 className="text-lg font-semibold text-white">
                  {selectedDocument.original_filename}
                </h3>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-400">
                <FaBookOpen className="w-4 h-4" />
                <span>Q&A Session Active</span>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="bg-dark-800/30 rounded-xl p-4 h-96 overflow-y-auto mb-4 space-y-3">
              {chatMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-xl ${
                      msg.type === 'user'
                        ? 'bg-primary-500 text-white'
                        : msg.type === 'ai'
                        ? 'bg-accent-500/20 text-white border border-accent-500/30'
                        : msg.type === 'system'
                        ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                        : 'bg-red-500/20 text-red-300 border border-red-500/30'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{msg.message}</p>
                    
                    {/* RAG Metadata Display */}
                    {msg.type === 'ai' && msg.ragMetadata && (
                      <div className="mt-2 pt-2 border-t border-gray-600/30">
                        <div className="flex items-center justify-between text-xs text-gray-400">
                          <div className="flex items-center space-x-2">
                            <FaRobot className="w-3 h-3" />
                            <span>
                              {msg.ragMetadata.rag_enabled ? 'RAG Enhanced' : 'Standard AI'}
                            </span>
                          </div>
                          {msg.ragMetadata.rag_enabled && (
                            <span className="text-emerald-400">
                              {msg.ragMetadata.chunks_retrieved || 0} chunks
                            </span>
                          )}
                        </div>
                        {msg.ragMetadata.rag_enabled && msg.ragMetadata.processing_method && (
                          <div className="text-xs text-gray-500 mt-1">
                            Method: {msg.ragMetadata.processing_method}
                          </div>
                        )}
                      </div>
                    )}
                    
                    <p className="text-xs opacity-70 mt-1">
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              {isAsking && (
                <div className="flex justify-start">
                  <div className="bg-accent-500/20 text-white border border-accent-500/30 px-4 py-2 rounded-xl">
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-accent-500"></div>
                      <span className="text-sm">AI is thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Question Input */}
            <div className="flex items-center space-x-3">
              <input
                type="text"
                value={currentQuestion}
                onChange={(e) => setCurrentQuestion(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !isAsking) {
                    askQuestion(currentQuestion);
                  }
                }}
                placeholder="Ask a question about this document..."
                className="flex-1 px-4 py-3 bg-dark-800/50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                disabled={isAsking}
              />
              <button
                onClick={() => askQuestion(currentQuestion)}
                disabled={isAsking || !currentQuestion.trim()}
                className="px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold rounded-xl hover:from-primary-600 hover:to-accent-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                <FaQuestionCircle className="w-4 h-4" />
                <span>Ask</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Q&A History */}
      {qaHistory.length > 0 && (
        <div className="glass-morphism rounded-2xl p-6">
          <h3 className="text-xl font-bold text-white mb-4">Recent Q&A History</h3>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {qaHistory.slice(0, 10).map((qa, index) => (
              <div key={index} className="p-3 bg-dark-800/50 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">{qa.document_filename}</span>
                  <span className="text-xs text-gray-500">
                    {new Date(qa.timestamp).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-sm text-white mb-1">Q: {qa.question}</p>
                <p className="text-sm text-gray-300 line-clamp-2">A: {qa.answer}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverview();
      case 'upload':
        return renderUpload();
      case 'library':
        return renderLibrary();
      case 'qa':
        return renderQA();
      case 'analytics':
        return (
          <div className="glass-morphism rounded-2xl p-8 text-center">
            <FaChartBar className="w-16 h-16 text-primary-400 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-white mb-2">Analytics Dashboard</h3>
            <p className="text-gray-400">Detailed analytics and insights coming soon!</p>
          </div>
        );
      case 'settings':
        return (
          <div className="glass-morphism rounded-2xl p-8 text-center">
            <FaCog className="w-16 h-16 text-accent-400 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-white mb-2">Settings</h3>
            <p className="text-gray-400">Customization options coming soon!</p>
          </div>
        );
      default:
        return renderOverview();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 flex">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-float"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-float animation-delay-400"></div>
      </div>

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-20'} glass-morphism transition-all duration-300 flex flex-col relative z-10`}>
        <div className="p-6">
          <div className="flex items-center space-x-3 mb-8">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl flex items-center justify-center animate-glow">
              <FaRobot className="w-6 h-6 text-white" />
            </div>
            {sidebarOpen && (
              <span className="text-xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
                RAG-LLM
              </span>
            )}
          </div>

          <nav className="space-y-2">
            {sidebarItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                  activeTab === item.id
                    ? 'bg-gradient-to-r from-primary-500/20 to-accent-500/20 text-white border border-primary-500/30'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <item.icon className="w-5 h-5" />
                {sidebarOpen && <span className="font-medium">{item.label}</span>}
              </button>
            ))}
          </nav>
        </div>

        <div className="mt-auto p-6">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="w-full flex items-center justify-center py-2 px-4 text-gray-400 hover:text-white transition-colors"
          >
            <svg className={`w-5 h-5 transition-transform ${sidebarOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative z-10">
        {/* Header */}
        <header className="glass-morphism border-b border-white/10 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-white">Dashboard</h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* Search Bar */}
              <div className="relative">
                <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search documents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 bg-dark-800/50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 w-64"
                />
              </div>

              {/* Notifications */}
              <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
                <FaBell className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
              </button>

              {/* User Menu */}
              <div className="flex items-center space-x-3">
                <Link to="/profile" className="flex items-center space-x-3 hover:bg-white/5 rounded-xl p-2 transition-colors">
                  <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
                    {currentUser?.photoURL ? (
                      <img src={currentUser.photoURL} alt="Profile" className="w-10 h-10 rounded-full object-cover" />
                    ) : (
                      <FaUser className="w-5 h-5 text-white" />
                    )}
                  </div>
                  <div className="hidden md:block">
                    <p className="text-white font-medium text-sm">
                      {userProfile?.displayName || currentUser?.displayName || 'User'}
                    </p>
                    <p className="text-gray-400 text-xs">Premium Member</p>
                  </div>
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-400 hover:text-red-400 transition-colors p-2"
                  title="Logout"
                >
                  <FaSignOutAlt className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 p-6 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;