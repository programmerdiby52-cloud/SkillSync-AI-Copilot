import streamlit as st
import random

# Comprehensive Mock Database for Certifications & Internships
# 10 Categories, Mix of Global and Indian opportunities
CERT_DATA = {
    "AI & Machine Learning": [
        {"title": "Google Professional ML Engineer", "type": "Certification", "level": "Advanced", "desc": "Design, build, and productionize ML models."},
        {"title": "OpenAI API Integration Internship", "type": "Internship", "level": "Intermediate", "desc": "Build GPT-4 wrappers for enterprise clients."},
        {"title": "DeepLearning.AI TensorFlow Developer", "type": "Certification", "level": "Intermediate", "desc": "Master neural networks and deep learning architectures."},
        {"title": "IBM AI Engineering Professional", "type": "Certification", "level": "Beginner", "desc": "Foundations of ML algorithms and Python data science."},
        {"title": "Computer Vision Research Intern (TCS Innovation)", "type": "Internship", "level": "Advanced", "desc": "Develop real-time object detection systems."}
    ],
    "Data Science": [
        {"title": "Microsoft Certified: Azure Data Scientist", "type": "Certification", "level": "Advanced", "desc": "Run ML workloads on Azure."},
        {"title": "Data Analytics Intern (KPMG India)", "type": "Internship", "level": "Beginner", "desc": "Analyze financial datasets using SQL and PowerBI."},
        {"title": "Google Data Analytics Certificate", "type": "Certification", "level": "Beginner", "desc": "Master R, SQL, and Tableau."},
        {"title": "Data Science Intern (Swiggy Tech)", "type": "Internship", "level": "Intermediate", "desc": "Optimize supply chain routing models."},
        {"title": "Databricks Certified Associate", "type": "Certification", "level": "Intermediate", "desc": "Master Apache Spark and Big Data pipelines."}
    ],
    "Web Development": [
        {"title": "Meta Front-End Developer", "type": "Certification", "level": "Beginner", "desc": "Master React, UI/UX principles, and JavaScript."},
        {"title": "Full Stack Intern (Razorpay)", "type": "Internship", "level": "Intermediate", "desc": "Build scalable Node.js microservices."},
        {"title": "AWS Certified Developer", "type": "Certification", "level": "Advanced", "desc": "Deploy and maintain cloud-native web apps."},
        {"title": "Next.js & Vercel Developer Intern", "type": "Internship", "level": "Intermediate", "desc": "Develop high-performance SSR frontends."},
        {"title": "IBM Full Stack Software Developer", "type": "Certification", "level": "Intermediate", "desc": "Cloud-native apps with React and Node."}
    ],
    "Mobile Development": [
        {"title": "Meta Android Developer", "type": "Certification", "level": "Beginner", "desc": "Build native applications using Kotlin."},
        {"title": "Meta iOS Developer", "type": "Certification", "level": "Beginner", "desc": "Master Swift and UIKIT."},
        {"title": "Flutter Developer Intern (Cred)", "type": "Internship", "level": "Intermediate", "desc": "Build smooth, animated cross-platform UI."},
        {"title": "Android Intern (Zomato)", "type": "Internship", "level": "Intermediate", "desc": "Optimize geographic location tracking modules."},
        {"title": "Associate Android Developer (Google)", "type": "Certification", "level": "Advanced", "desc": "Industry-standard certification for Android."}
    ],
    "Cybersecurity": [
        {"title": "CompTIA Security+", "type": "Certification", "level": "Beginner", "desc": "Global standard for validating baseline security skills."},
        {"title": "Certified Ethical Hacker (CEH)", "type": "Certification", "level": "Advanced", "desc": "Master penetration testing and exploit writing."},
        {"title": "Security Analyst Intern (Infosys)", "type": "Internship", "level": "Intermediate", "desc": "Monitor network traffic for vulnerability detection."},
        {"title": "Google Cybersecurity Certificate", "type": "Certification", "level": "Beginner", "desc": "Foundational skills in SIEM and Python security scripts."},
        {"title": "Pen-Testing Intern (CrowdStrike)", "type": "Internship", "level": "Advanced", "desc": "Simulate adversary attacks on enterprise environments."}
    ],
    "Cloud Computing": [
        {"title": "AWS Solutions Architect Associate", "type": "Certification", "level": "Intermediate", "desc": "Design scalable and highly available AWS systems."},
        {"title": "Google Cloud Associate Engineer", "type": "Certification", "level": "Intermediate", "desc": "Deploy apps, monitor operations, and manage GCP."},
        {"title": "Cloud Migration Intern (Wipro)", "type": "Internship", "level": "Beginner", "desc": "Assist in migrating legacy SQL to AWS RDS."},
        {"title": "Microsoft Azure Fundamentals (AZ-900)", "type": "Certification", "level": "Beginner", "desc": "Core understanding of Azure services."},
        {"title": "Cloud Infrastructure Intern (AWS India)", "type": "Internship", "level": "Advanced", "desc": "Automate infrastructure deployment using Terraform."}
    ],
    "DevOps": [
        {"title": "Certified Kubernetes Administrator (CKA)", "type": "Certification", "level": "Advanced", "desc": "Configure and manage production K8s clusters."},
        {"title": "DevOps Engineering Intern (Postman)", "type": "Internship", "level": "Intermediate", "desc": "Maintain CI/CD pipelines via GitHub Actions."},
        {"title": "Docker Certified Associate", "type": "Certification", "level": "Intermediate", "desc": "Master containerization and Docker Swarm."},
        {"title": "AWS DevOps Engineer Professional", "type": "Certification", "level": "Advanced", "desc": "Implement and manage continuous delivery."},
        {"title": "SRE Intern (Atlassian)", "type": "Internship", "level": "Advanced", "desc": "Build observability tools using Prometheus/Grafana."}
    ],
    "Blockchain": [
        {"title": "Certified Blockchain Developer (CBD)", "type": "Certification", "level": "Intermediate", "desc": "Build smart contracts on Ethereum using Solidity."},
        {"title": "Web3 Developer Intern (Polygon)", "type": "Internship", "level": "Advanced", "desc": "Develop dApps on Polygon Layer 2."},
        {"title": "Hyperledger Fabric Developer", "type": "Certification", "level": "Advanced", "desc": "Build permissioned enterprise blockchain networks."},
        {"title": "DeFi Research Intern", "type": "Internship", "level": "Intermediate", "desc": "Analyze liquidity pools and smart contract security."},
        {"title": "Blockchain Essentials (IBM)", "type": "Certification", "level": "Beginner", "desc": "Understand core DLT and cryptographic hashing."}
    ],
    "UI/UX Design": [
        {"title": "Google UX Design Certificate", "type": "Certification", "level": "Beginner", "desc": "Wireframing, prototyping, and user research."},
        {"title": "Product Design Intern (Zoho)", "type": "Internship", "level": "Intermediate", "desc": "Design SaaS dashboards and mobile interfaces."},
        {"title": "Figma Advanced Component Libraries", "type": "Certification", "level": "Intermediate", "desc": "Master auto-layout, design tokens, and components."},
        {"title": "UI Intern (Cure.fit)", "type": "Internship", "level": "Intermediate", "desc": "Create micro-animations and accessibility features."},
        {"title": "Interaction Design Foundation (IDF)", "type": "Certification", "level": "Advanced", "desc": "Psychology of human-computer interaction."}
    ],
    "Core Engineering": [
        {"title": "AutoCAD Professional Certification", "type": "Certification", "level": "Intermediate", "desc": "Advanced 2D/3D drafting and design."},
        {"title": "Embedded Systems Intern (Bosch)", "type": "Internship", "level": "Advanced", "desc": "Program microcontrollers for automotive IoT."},
        {"title": "IoT Developer (Cisco)", "type": "Certification", "level": "Intermediate", "desc": "Connect edge devices to cloud infrastructure."},
        {"title": "Robotics Engineering Intern (GreyOrange)", "type": "Internship", "level": "Advanced", "desc": "Program warehouse automation pathfinding algorithms."},
        {"title": "MATLAB Associate", "type": "Certification", "level": "Beginner", "desc": "Core numerical computing and data visualization."}
    ]
}

def render_certs():
    st.markdown("""
        <div style="animation: fadeSlideUp 0.6s ease-out;">
            <h2 style="margin-bottom: 5px; font-weight: 700;">Certifications & Internships</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px;">Discover highly-vetted global and Indian opportunities mapped to your targeted career field.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Render Tabs for the 10 Categories
    tabs = st.tabs(list(CERT_DATA.keys()))
    
    for i, (category, items) in enumerate(CERT_DATA.items()):
        with tabs[i]:
            st.markdown(f"### Top Opportunities in {category}")
            st.write("---")
            
            # Dynamic Reshuffle Logic on every render!
            shuffled_items = list(items)
            random.shuffle(shuffled_items)
            
            # Create a 2-column grid for the cards
            col1, col2 = st.columns(2, gap="medium")
            
            for idx, item in enumerate(shuffled_items):
                target_col = col1 if idx % 2 == 0 else col2
                
                # Pill styling based on Type and Level
                type_color = "var(--accent-gradient)" if item['type'] == 'Certification' else "#10B981"
                level_color = "#3B82F6" if item['level'] == 'Beginner' else ("#F59E0B" if item['level'] == 'Intermediate' else "#EF4444")
                
                with target_col:
                    st.markdown(f"""
                    <div style="background: var(--surface-color); border: 1px solid var(--border-color); border-radius: 16px; padding: 20px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: transform 0.3s ease, box-shadow 0.3s ease;" class="cert-card">
                        <div>
                            <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                                <span style="background: {type_color}; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">{item['type']}</span>
                                <span style="background: {level_color}; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">{item['level']}</span>
                            </div>
                            <h4 style="margin: 0 0 10px 0; font-size: 16px; font-weight: 600; line-height: 1.3;">{item['title']}</h4>
                            <p style="color: var(--text-secondary); font-size: 13px; line-height: 1.5; margin-bottom: 20px;">{item['desc']}</p>
                        </div>
                        <button style="width: 100%; background: transparent; color: var(--text-primary); border: 1px solid var(--border-color); border-radius: 8px; padding: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s ease;">View Opportunity →</button>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

# Add custom hover CSS specifically for these cards via standard streamlit markdown injection
st.markdown("""
<style>
    .cert-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 0 15px rgba(59, 130, 246, 0.1) !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)
