# frontend/styles.py
def get_css_styles():
    """Retorna los estilos CSS personalizados"""
    return """
    <style>
        .encabezado {
            background: #42001A;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }
        
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .dashboard-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1f4e79, #2d5a87);
        }
        
        .success-message {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .error-message {
            background: linear-gradient(90deg, #f44336, #d32f2f);
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .info-message {
            background: linear-gradient(90deg, #2196F3, #1976D2);
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .warning-message {
            background: linear-gradient(90deg, #FF9800, #F57C00);
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .form-container {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .chart-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        
        .user-profile {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .offer-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        
        .offer-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .compatibility-badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .compatibility-high {
            background: #4CAF50;
            color: white;
        }
        
        .compatibility-medium {
            background: #FF9800;
            color: white;
        }
        
        .compatibility-low {
            background: #f44336;
            color: white;
        }
        
        .skill-tag {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin: 0.1rem;
        }
        
        .navbar {
            background: linear-gradient(90deg, #1f4e79, #2d5a87);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .navbar h1 {
            color: white;
            margin: 0;
            text-align: center;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-top: 2rem;
            border-top: 1px solid #dee2e6;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .login-container {
                max-width: 100%;
                margin: 0;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .metric-card {
                margin-bottom: 1rem;
            }
        }
        
        /* Animaciones */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        /* Scrollbar personalizada */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #1f4e79;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #2d5a87;
        }
    </style>
    """
