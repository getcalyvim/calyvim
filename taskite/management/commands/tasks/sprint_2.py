tasks = [
    {
        "summary": "Implement advanced user roles and permissions",
        "description": "Create a flexible role-based access control system with customizable permissions and hierarchical role structure",
        "assignee_count": 3,
        "labels_count": 4,
        "comments": [
            "Consider using Django Guardian",
            "Need audit logging for permission changes",
        ],
        "subtasks": [
            {
                "summary": "Design permission structure",
                "description": "Create comprehensive permission hierarchy and role templates",
                "assignee_count": 1,
                "labels_count": 2,
                "comments": ["Include role inheritance"],
            },
            {
                "summary": "Implement permission UI",
                "description": "Create interface for managing roles and permissions",
                "assignee_count": 2,
                "labels_count": 1,
                "comments": ["Make it user-friendly for admins"],
            },
        ],
    },
    {
        "summary": "Add collaborative document editing",
        "description": "Implement real-time collaborative document editing with version control and conflict resolution",
        "assignee_count": 3,
        "labels_count": 3,
        "comments": [
            "Consider using Operational Transform",
            "Implement auto-save feature",
        ],
        "subtasks": [
            {
                "summary": "Implement document locking",
                "description": "Create mechanism for handling concurrent edits",
                "assignee_count": 1,
                "labels_count": 2,
                "comments": ["Use Redis for lock management"],
            }
        ],
    },
    {
        "summary": "Create workflow automation system",
        "description": "Build a system for creating and managing automated workflows with custom triggers and actions",
        "assignee_count": 2,
        "labels_count": 3,
        "comments": ["Use Apache Airflow", "Include visual workflow builder"],
        "subtasks": [],
    },
    {
        "summary": "Implement advanced report generation",
        "description": "Create customizable report generation system with multiple templates and export options",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Use ReportLab for PDF generation", "Add scheduling capabilities"],
        "subtasks": [],
    },
    {
        "summary": "Add audit logging dashboard",
        "description": "Create comprehensive dashboard for viewing and analyzing system audit logs",
        "assignee_count": 2,
        "labels_count": 3,
        "comments": ["Implement advanced filtering", "Add export functionality"],
        "subtasks": [],
    },
    {
        "summary": "Implement data import system",
        "description": "Create robust data import system supporting multiple file formats with validation and error handling",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Support CSV, Excel, and JSON", "Add data mapping interface"],
        "subtasks": [],
    },
    {
        "summary": "Add advanced search filters",
        "description": "Enhance search functionality with advanced filters, saved searches, and search history",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Implement faceted search", "Add search analytics"],
        "subtasks": [],
    },
    {
        "summary": "Implement team collaboration features",
        "description": "Add team workspace features including shared documents, team chat, and task management",
        "assignee_count": 3,
        "labels_count": 3,
        "comments": ["Include team analytics", "Add resource sharing"],
        "subtasks": [],
    },
    {
        "summary": "Create API rate plan management",
        "description": "Implement system for managing different API rate plans and usage tracking",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Include usage analytics", "Add automated billing"],
        "subtasks": [],
    },
    {
        "summary": "Add custom dashboard builder",
        "description": "Create drag-and-drop interface for building custom dashboards with widgets",
        "assignee_count": 3,
        "labels_count": 3,
        "comments": ["Use React DnD", "Include widget library"],
        "subtasks": [],
    },
    {
        "summary": "Implement advanced caching system",
        "description": "Create multi-layer caching system with cache invalidation and prefetching",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Use Redis and Memcached", "Implement cache warming"],
        "subtasks": [],
    },
    {
        "summary": "Add automated testing framework",
        "description": "Implement comprehensive automated testing framework including unit, integration, and E2E tests",
        "assignee_count": 2,
        "labels_count": 3,
        "comments": ["Use Jest and Cypress", "Add CI/CD integration"],
        "subtasks": [],
    },
    {
        "summary": "Create user feedback system",
        "description": "Implement system for collecting and managing user feedback and feature requests",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Include sentiment analysis", "Add feedback categorization"],
        "subtasks": [],
    },
    {
        "summary": "Implement AI-powered recommendations",
        "description": "Add machine learning-based recommendation system for content and features",
        "assignee_count": 3,
        "labels_count": 3,
        "comments": ["Use TensorFlow", "Implement A/B testing"],
        "subtasks": [],
    },
    {
        "summary": "Add compliance reporting system",
        "description": "Create system for generating compliance reports and monitoring regulatory requirements",
        "assignee_count": 2,
        "labels_count": 3,
        "comments": ["Include GDPR requirements", "Add automated alerts"],
        "subtasks": [],
    },
    {
        "summary": "Implement service health monitoring",
        "description": "Create comprehensive system monitoring dashboard with alerts and incident management",
        "assignee_count": 2,
        "labels_count": 2,
        "comments": ["Use Prometheus and Grafana", "Add incident response workflow"],
        "subtasks": [],
    },
]