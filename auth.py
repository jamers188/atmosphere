import streamlit as st
import bcrypt
import json
import os
import time
from datetime import datetime, timedelta
from PIL import Image
import random
import uuid
import base64
from io import BytesIO

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Atmosphere",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== PREMIUM UI STYLING =====
def load_css():
    st.markdown("""
    <style>
        /* Main Design System & Variables */
        :root {
            /* Color System - Core */
            --primary: #3a86ff;
            --primary-hover: #2a76ef;
            --primary-light: #8bb9ff;
            --primary-dark: #0056e0;
            --secondary: #4cc9f0;
            --secondary-hover: #30b9e5;
            --accent: #ff006e;
            --accent-hover: #e5005e;
            --success: #38b000;
            --warning: #ffbe0b;
            --error: #ff5964;
            --info: #3a86ff;
            
            /* Color System - Neutrals */
            --neutral-50: #f8fafc;
            --neutral-100: #f1f5f9;
            --neutral-200: #e2e8f0;
            --neutral-300: #cbd5e1;
            --neutral-400: #94a3b8;
            --neutral-500: #64748b;
            --neutral-600: #475569;
            --neutral-700: #334155;
            --neutral-800: #1e293b;
            --neutral-900: #0f172a;
            
            /* Gradient Palettes */
            --gradient-blue: linear-gradient(135deg, #3a86ff 0%, #4cc9f0 100%);
            --gradient-purple: linear-gradient(135deg, #8338ec 0%, #3a86ff 100%);
            --gradient-pink: linear-gradient(135deg, #ff006e 0%, #8338ec 100%);
            --gradient-sunset: linear-gradient(135deg, #ffbe0b 0%, #ff006e 100%);
            
            /* Dark Mode Gradients */
            --gradient-dark-blue: linear-gradient(135deg, #0d47a1 0%, #0277bd 100%);
            --gradient-dark-purple: linear-gradient(135deg, #4a148c 0%, #311b92 100%);
            
            /* Typography */
            --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            --font-heading: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            
            /* Spacing */
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-5: 1.25rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --space-10: 2.5rem;
            --space-12: 3rem;
            --space-16: 4rem;
            --space-20: 5rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
            
            /* Border Radius */
            --radius-sm: 0.125rem;
            --radius: 0.25rem;
            --radius-md: 0.375rem;
            --radius-lg: 0.5rem;
            --radius-xl: 0.75rem;
            --radius-2xl: 1rem;
            --radius-3xl: 1.5rem;
            --radius-full: 9999px;
            
            /* Transition */
            --transition-all: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-colors: background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1), color 0.2s cubic-bezier(0.4, 0, 0.2, 1), fill 0.2s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-opacity: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-shadow: box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-transform: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            
            /* Z-Index */
            --z-0: 0;
            --z-10: 10;
            --z-20: 20;
            --z-30: 30;
            --z-40: 40;
            --z-50: 50;
            --z-auto: auto;
        }
        
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Poppins:wght@400;500;600;700&display=swap');
        
        /* Base Styles */
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: var(--font-primary);
            color: var(--neutral-800);
            background-color: var(--neutral-50);
            transition: var(--transition-colors);
            position: relative;
            min-height: 100vh;
            line-height: 1.6;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-heading);
            font-weight: 600;
            color: var(--neutral-900);
            line-height: 1.25;
            scroll-margin-top: 100px;
        }
        
        h1 {
            font-size: 2.25rem;
            letter-spacing: -0.025em;
            font-weight: 700;
        }
        
        h2 {
            font-size: 1.875rem;
            letter-spacing: -0.025em;
        }
        
        h3 {
            font-size: 1.5rem;
            letter-spacing: -0.025em;
        }
        
        h4 {
            font-size: 1.25rem;
        }
        
        h5 {
            font-size: 1.125rem;
        }
        
        h6 {
            font-size: 1rem;
        }
        
        p {
            color: var(--neutral-700);
            margin-bottom: 1rem;
        }
        
        a {
            color: var(--primary);
            text-decoration: none;
            transition: var(--transition-colors);
        }
        
        a:hover {
            color: var(--primary-hover);
            text-decoration: none;
        }
        
        hr {
            border: 0;
            height: 1px;
            background-color: var(--neutral-200);
            margin: 1.5rem 0;
        }
        
        code, pre {
            font-family: var(--font-mono);
            font-size: 0.9em;
            background-color: var(--neutral-100);
            border-radius: var(--radius-md);
        }
        
        code {
            padding: 0.2em 0.4em;
        }
        
        pre {
            padding: 1rem;
            overflow-x: auto;
        }
        
        blockquote {
            border-left: 3px solid var(--primary);
            padding-left: 1rem;
            font-style: italic;
            color: var(--neutral-600);
        }
        
        /* Streamlit specific overrides */
        .stButton>button {
            background: var(--primary) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-lg) !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.25rem !important;
            font-family: var(--font-primary) !important;
            transition: var(--transition-all) !important;
            box-shadow: var(--shadow) !important;
            height: auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.5rem !important;
        }
        
        .stButton>button:hover {
            background: var(--primary-hover) !important;
            box-shadow: var(--shadow-md) !important;
            transform: translateY(-1px) !important;
        }
        
        .stButton>button:active {
            transform: translateY(0) !important;
            box-shadow: var(--shadow) !important;
        }
        
        /* Secondary button style */
        .btn-secondary>button {
            background: white !important;
            color: var(--primary) !important;
            border: 1px solid var(--primary) !important;
        }
        
        .btn-secondary>button:hover {
            background: var(--neutral-50) !important;
        }
        
        /* Danger button style */
        .btn-danger>button {
            background: var(--error) !important;
        }
        
        .btn-danger>button:hover {
            background: #e54954 !important;
        }
        
        /* Text inputs */
        div[data-baseweb="input"] {
            border-radius: var(--radius-lg) !important;
            transition: var(--transition-all) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        div[data-baseweb="input"]:hover {
            box-shadow: var(--shadow) !important;
        }
        
        div[data-baseweb="input"]:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(58, 134, 255, 0.25) !important;
        }
        
        /* Select boxes */
        div[data-baseweb="select"] {
            border-radius: var(--radius-lg) !important;
            transition: var(--transition-all) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        div[data-baseweb="select"]:hover {
            box-shadow: var(--shadow) !important;
        }
        
        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(58, 134, 255, 0.25) !important;
        }
        
        /* Checkbox */
        label[data-baseweb="checkbox"] {
            gap: 8px !important;
        }
        
        /* Metrics */
        div[data-testid="stMetricValue"] {
            font-family: var(--font-heading) !important;
            font-weight: 600 !important;
            color: var(--primary) !important;
        }
        
        div[data-testid="stMetricLabel"] {
            color: var(--neutral-600) !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: var(--gradient-blue) !important;
            color: white !important;
        }
        
        section[data-testid="stSidebar"] button {
            background: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border: none !important;
            transition: var(--transition-all) !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: rgba(255, 255, 255, 0.3) !important;
        }
        
        section[data-testid="stSidebar"] hr {
            background-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stMarkdown"] p {
            color: rgba(255, 255, 255, 0.8) !important;
        }
        
        /* Radio buttons */
        div[role="radiogroup"] label {
            padding: 0.5rem 1rem !important;
            border-radius: var(--radius) !important;
            transition: var(--transition-all) !important;
        }
        
        div[role="radiogroup"] label:hover {
            background: var(--neutral-100) !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
            border-bottom: 1px solid var(--neutral-200) !important;
            margin-bottom: 1rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: var(--radius) var(--radius) 0 0 !important;
            padding: 0.75rem 1rem !important;
            font-weight: 500 !important;
            color: var(--neutral-600) !important;
            border: none !important;
            transition: var(--transition-colors) !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--primary) !important;
            background: var(--neutral-50) !important;
        }
        
        .stTabs [aria-selected="true"] {
            color: var(--primary) !important;
            font-weight: 600 !important;
            border-bottom: 2px solid var(--primary) !important;
            background: transparent !important;
        }
        
        /* Expanders */
        [data-testid="stExpander"] {
            border: 1px solid var(--neutral-200) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden !important;
            transition: var(--transition-all) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        [data-testid="stExpander"]:hover {
            box-shadow: var(--shadow) !important;
        }
        
        [data-testid="stExpander"] > div:first-child {
            background: var(--neutral-50) !important;
            padding: 1rem !important;
        }
        
        /* Custom components styling */
        /* Cards */
        .card {
            background: white;
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
            position: relative;
            overflow: hidden;
            height: 100%;
        }
        
        .card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .card-title {
            font-family: var(--font-heading);
            font-weight: 600;
            font-size: 1.25rem;
            margin-bottom: var(--space-4);
            color: var(--neutral-900);
        }
        
        .card-subtitle {
            font-size: 0.875rem;
            color: var(--neutral-600);
            margin-bottom: var(--space-4);
        }
        
        .card-content {
            margin-bottom: var(--space-4);
        }
        
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
        }
        
        .card-footer-info {
            font-size: 0.875rem;
            color: var(--neutral-500);
        }
        
        .card-badge {
            position: absolute;
            top: var(--space-4);
            right: var(--space-4);
            background: var(--primary);
            color: white;
            padding: var(--space-1) var(--space-3);
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        /* Premium card with gradient border */
        .card-premium {
            position: relative;
            border-radius: var(--radius-xl);
            padding: 2px; /* Border width */
            background: var(--gradient-blue);
        }
        
        .card-premium-inner {
            background: white;
            border-radius: calc(var(--radius-xl) - 2px);
            padding: var(--space-6);
            height: 100%;
        }
        
        /* Activity card */
        .activity-item {
            display: flex;
            align-items: flex-start;
            padding: var(--space-4);
            background: var(--neutral-50);
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-3);
            transition: var(--transition-all);
        }
        
        .activity-item:hover {
            background: var(--neutral-100);
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }
        
        .activity-icon {
            flex-shrink: 0;
            width: 40px;
            height: 40px;
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: var(--space-4);
            background: var(--primary);
            color: white;
            font-size: 1.25rem;
        }
        
        .activity-content {
            flex-grow: 1;
        }
        
        .activity-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--space-1);
        }
        
        .activity-title {
            font-weight: 600;
            color: var(--neutral-800);
        }
        
        .activity-time {
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        .activity-description {
            color: var(--neutral-600);
            font-size: 0.9rem;
            margin-bottom: var(--space-2);
        }
        
        .activity-meta {
            display: flex;
            gap: var(--space-3);
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        /* Stats card */
        .stat-card {
            background: white;
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
            height: 100%;
        }
        
        .stat-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: var(--radius);
            background: var(--primary-light);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: var(--space-3);
        }
        
        .stat-value {
            font-family: var(--font-heading);
            font-size: 2rem;
            font-weight: 700;
            color: var(--neutral-900);
            line-height: 1.2;
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: var(--neutral-600);
            margin-top: var(--space-1);
        }
        
        .stat-change {
            display: flex;
            align-items: center;
            margin-top: var(--space-2);
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .stat-change.positive {
            color: var(--success);
        }
        
        .stat-change.negative {
            color: var(--error);
        }
        
        /* Profile card */
        .profile-card {
            display: flex;
            align-items: center;
            padding: var(--space-4);
            background: white;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
        }
        
        .profile-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .profile-avatar {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: var(--space-4);
            border: 2px solid var(--primary);
        }
        
        .profile-info {
            flex-grow: 1;
        }
        
        .profile-name {
            font-family: var(--font-heading);
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--neutral-900);
            margin-bottom: var(--space-1);
        }
        
        .profile-role {
            font-size: 0.875rem;
            color: var(--primary);
            margin-bottom: var(--space-2);
        }
        
        .profile-meta {
            display: flex;
            gap: var(--space-3);
            font-size: 0.75rem;
            color: var(--neutral-600);
        }
        
        /* Badge */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: var(--space-1) var(--space-3);
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            font-weight: 500;
            color: white;
        }
        
        .badge-primary {
            background: var(--primary);
        }
        
        .badge-secondary {
            background: var(--secondary);
        }
        
        .badge-success {
            background: var(--success);
        }
        
        .badge-warning {
            background: var(--warning);
            color: var(--neutral-900);
        }
        
        .badge-error {
            background: var(--error);
        }
        
        .badge-neutral {
            background: var(--neutral-200);
            color: var(--neutral-700);
        }
        
        /* Progress bar */
        .progress-container {
            width: 100%;
            height: 8px;
            background: var(--neutral-200);
            border-radius: var(--radius-full);
            overflow: hidden;
            margin: var(--space-2) 0;
        }
        
        .progress-bar {
            height: 100%;
            background: var(--primary);
            border-radius: var(--radius-full);
            transition: width 0.5s ease;
        }
        
        /* Modal */
        .modal-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: var(--z-50);
            backdrop-filter: blur(4px);
        }
        
        .modal {
            background: white;
            border-radius: var(--radius-xl);
            width: 90%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: var(--shadow-xl);
            animation: modalFadeIn 0.3s ease;
        }
        
        .modal-header {
            padding: var(--space-6);
            border-bottom: 1px solid var(--neutral-200);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-title {
            font-family: var(--font-heading);
            font-weight: 600;
            font-size: 1.25rem;
            color: var(--neutral-900);
        }
        
        .modal-close {
            background: transparent;
            border: none;
            color: var(--neutral-500);
            font-size: 1.5rem;
            cursor: pointer;
            transition: var(--transition-colors);
        }
        
        .modal-close:hover {
            color: var(--neutral-700);
        }
        
        .modal-body {
            padding: var(--space-6);
        }
        
        .modal-footer {
            padding: var(--space-6);
            border-top: 1px solid var(--neutral-200);
            display: flex;
            justify-content: flex-end;
            gap: var(--space-3);
        }
        
        @keyframes modalFadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Toast notifications */
        .toast {
            position: fixed;
            bottom: var(--space-6);
            right: var(--space-6);
            padding: var(--space-4);
            border-radius: var(--radius-lg);
            background: white;
            box-shadow: var(--shadow-lg);
            display: flex;
            align-items: center;
            gap: var(--space-3);
            min-width: 300px;
            max-width: 450px;
            z-index: var(--z-50);
            animation: toastFadeIn 0.5s ease;
        }
        
        .toast-icon {
            flex-shrink: 0;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.875rem;
        }
        
        .toast-success .toast-icon {
            background: var(--success);
            color: white;
        }
        
        .toast-error .toast-icon {
            background: var(--error);
            color: white;
        }
        
        .toast-warning .toast-icon {
            background: var(--warning);
            color: var(--neutral-900);
        }
        
        .toast-info .toast-icon {
            background: var(--info);
            color: white;
        }
        
        .toast-content {
            flex-grow: 1;
        }
        
        .toast-title {
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--neutral-900);
            margin-bottom: var(--space-1);
        }
        
        .toast-message {
            font-size: 0.8125rem;
            color: var(--neutral-600);
        }
        
        .toast-close {
            flex-shrink: 0;
            background: transparent;
            border: none;
            color: var(--neutral-500);
            cursor: pointer;
            padding: var(--space-1);
            transition: var(--transition-colors);
        }
        
        .toast-close:hover {
            color: var(--neutral-700);
        }
        
        @keyframes toastFadeIn {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip-content {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: var(--space-2) var(--space-3);
            background: var(--neutral-800);
            color: white;
            border-radius: var(--radius);
            font-size: 0.75rem;
            white-space: nowrap;
            z-index: var(--z-50);
            opacity: 0;
            pointer-events: none;
            transition: var(--transition-all);
            margin-bottom: var(--space-2);
            visibility: hidden;
        }
        
        .tooltip:hover .tooltip-content {
            opacity: 1;
            visibility: visible;
        }
        
        .tooltip-content::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 4px;
            border-style: solid;
            border-color: var(--neutral-800) transparent transparent transparent;
        }
        
        /* Tag / Chip */
        .tag {
            display: inline-flex;
            align-items: center;
            gap: var(--space-1);
            padding: var(--space-1) var(--space-3);
            background: var(--neutral-100);
            color: var(--neutral-700);
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            font-weight: 500;
            transition: var(--transition-all);
        }
        
        .tag:hover {
            background: var(--neutral-200);
        }
        
        .tag-primary {
            background: rgba(58, 134, 255, 0.1);
            color: var(--primary);
        }
        
        .tag-primary:hover {
            background: rgba(58, 134, 255, 0.2);
        }
        
        .tag-remove {
            background: transparent;
            border: none;
            color: currentColor;
            cursor: pointer;
            font-size: 0.75rem;
            opacity: 0.7;
            transition: var(--transition-opacity);
            padding: 0;
            margin-left: var(--space-1);
        }
        
        .tag-remove:hover {
            opacity: 1;
        }
        
        /* Avatar */
        .avatar {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 500;
            color: white;
            border-radius: 50%;
            background: var(--primary);
        }
        
        .avatar-sm {
            width: 24px;
            height: 24px;
            font-size: 0.625rem;
        }
        
        .avatar-md {
            width: 36px;
            height: 36px;
            font-size: 0.75rem;
        }
        
        .avatar-lg {
            width: 48px;
            height: 48px;
            font-size: 1rem;
        }
        
        .avatar-xl {
            width: 64px;
            height: 64px;
            font-size: 1.25rem;
        }
        
        .avatar-status {
            position: absolute;
            bottom: 0;
            right: 0;
            width: 25%;
            height: 25%;
            border-radius: 50%;
            border: 2px solid white;
        }
        
        .avatar-status-online {
            background: var(--success);
        }
        
        .avatar-status-busy {
            background: var(--error);
        }
        
        .avatar-status-away {
            background: var(--warning);
        }
        
        .avatar-group {
            display: inline-flex;
        }
        
        .avatar-group .avatar {
            border: 2px solid white;
            margin-left: -0.5rem;
            transition: var(--transition-transform);
        }
        
        .avatar-group .avatar:first-child {
            margin-left: 0;
        }
        
        .avatar-group:hover .avatar {
            transform: translateX(0) !important;
        }
        
        .avatar-group .avatar:hover {
            z-index: 1;
            transform: scale(1.1) !important;
        }
        
        /* Timeline */
        .timeline {
            position: relative;
            padding-left: 2rem;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            left: 8px;
            width: 2px;
            background: var(--neutral-200);
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: var(--space-6);
        }
        
        .timeline-item:last-child {
            margin-bottom: 0;
        }
        
        .timeline-dot {
            position: absolute;
            top: 4px;
            left: -2rem;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--primary);
            border: 3px solid white;
            z-index: 1;
        }
        
        .timeline-content {
            background: white;
            border-radius: var(--radius-lg);
            padding: var(--space-4);
            box-shadow: var(--shadow-md);
        }
        
        .timeline-date {
            font-size: 0.75rem;
            color: var(--neutral-500);
            margin-bottom: var(--space-2);
        }
        
        .timeline-title {
            font-weight: 600;
            margin-bottom: var(--space-2);
            color: var(--neutral-900);
        }
        
        .timeline-body {
            color: var(--neutral-700);
            font-size: 0.9rem;
        }
        
        /* Map marker */
        .map-marker {
            width: 36px;
            height: 36px;
            border-radius: 50% 50% 50% 0;
            background: var(--primary);
            position: absolute;
            transform: rotate(-45deg);
            left: 50%;
            top: 50%;
            margin: -15px 0 0 -15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: var(--shadow-md);
        }
        
        .map-marker::after {
            content: '';
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: white;
            position: absolute;
            transform: translate(-50%, -50%);
            left: 50%;
            top: 50%;
        }
        
        .map-marker-content {
            position: relative;
            transform: rotate(45deg);
            font-size: 0.75rem;
            font-weight: 600;
            z-index: 1;
        }
        
        /* Search bar */
        .search-container {
            position: relative;
        }
        
        .search-input {
            width: 100%;
            padding: var(--space-3) var(--space-3) var(--space-3) calc(2.25rem + var(--space-3));
            border: 1px solid var(--neutral-300);
            border-radius: var(--radius-full);
            transition: var(--transition-all);
            font-size: 0.875rem;
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(58, 134, 255, 0.25);
        }
        
        .search-icon {
            position: absolute;
            left: var(--space-3);
            top: 50%;
            transform: translateY(-50%);
            color: var(--neutral-500);
        }
        
        /* Event card */
        .event-card {
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .event-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .event-image {
            height: 140px;
            overflow: hidden;
            position: relative;
        }
        
        .event-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        
        .event-card:hover .event-image img {
            transform: scale(1.05);
        }
        
        .event-date-badge {
            position: absolute;
            top: var(--space-3);
            right: var(--space-3);
            background: white;
            color: var(--neutral-900);
            border-radius: var(--radius);
            padding: var(--space-2) var(--space-3);
            font-weight: 600;
            font-size: 0.75rem;
            box-shadow: var(--shadow);
        }
        
        .event-content {
            padding: var(--space-5);
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .event-meta {
            display: flex;
            align-items: center;
            gap: var(--space-2);
            margin-bottom: var(--space-3);
        }
        
        .event-category {
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--primary);
        }
        
        .event-dot {
            width: 3px;
            height: 3px;
            background: var(--neutral-400);
            border-radius: 50%;
        }
        
        .event-time {
            font-size: 0.75rem;
            color: var(--neutral-600);
        }
        
        .event-title {
            font-weight: 600;
            font-size: 1.125rem;
            margin-bottom: var(--space-3);
            color: var(--neutral-900);
            line-height: 1.4;
        }
        
        .event-description {
            font-size: 0.875rem;
            color: var(--neutral-600);
            margin-bottom: var(--space-4);
        }
        
        .event-footer {
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--neutral-200);
            padding-top: var(--space-4);
        }
        
        .event-location {
            display: flex;
            align-items: center;
            gap: var(--space-2);
            font-size: 0.875rem;
            color: var(--neutral-600);
        }
        
        .event-attendees {
            display: flex;
            align-items: center;
        }
        
        /* Media gallery */
        .gallery-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: var(--space-4);
        }
        
        .gallery-item {
            border-radius: var(--radius-lg);
            overflow: hidden;
            aspect-ratio: 1 / 1;
            position: relative;
            box-shadow: var(--shadow);
            transition: var(--transition-all);
        }
        
        .gallery-item:hover {
            box-shadow: var(--shadow-lg);
            transform: scale(1.02);
            z-index: 1;
        }
        
        .gallery-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        
        .gallery-item:hover .gallery-image {
            transform: scale(1.05);
        }
        
        .gallery-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: var(--space-3);
            background: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0));
            color: white;
            opacity: 0;
            transform: translateY(10px);
            transition: var(--transition-all);
        }
        
        .gallery-item:hover .gallery-overlay {
            opacity: 1;
            transform: translateY(0);
        }
        
        .gallery-title {
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: var(--space-1);
        }
        
        .gallery-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            opacity: 0.8;
        }
        
        /* Circle cards */
        .circle-card {
            display: flex;
            flex-direction: column;
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
            height: 100%;
        }
        
        .circle-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .circle-banner {
            height: 80px;
            background: var(--gradient-blue);
            position: relative;
        }
        
        .circle-avatar {
            position: absolute;
            bottom: 0;
            left: var(--space-5);
            transform: translateY(50%);
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1.5rem;
            color: var(--primary);
            border: 3px solid white;
            box-shadow: var(--shadow);
        }
        
        .circle-content {
            padding: var(--space-5);
            padding-top: calc(64px / 2 + var(--space-5));
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .circle-title {
            font-weight: 600;
            font-size: 1.125rem;
            margin-bottom: var(--space-2);
            color: var(--neutral-900);
        }
        
        .circle-description {
            font-size: 0.875rem;
            color: var(--neutral-600);
            margin-bottom: var(--space-4);
        }
        
        .circle-stats {
            display: flex;
            gap: var(--space-4);
            margin-bottom: var(--space-4);
        }
        
        .circle-stat {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .circle-stat-value {
            font-weight: 600;
            color: var(--neutral-900);
        }
        
        .circle-stat-label {
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        .circle-tags {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-2);
            margin-bottom: var(--space-4);
        }
        
        .circle-footer {
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .circle-privacy {
            font-size: 0.75rem;
            color: var(--neutral-500);
            display: flex;
            align-items: center;
            gap: var(--space-1);
        }
        
        /* Business card */
        .business-card {
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
            height: 100%;
        }
        
        .business-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .business-header {
            display: flex;
            padding: var(--space-5);
            border-bottom: 1px solid var(--neutral-200);
        }
        
        .business-logo {
            width: 56px;
            height: 56px;
            border-radius: var(--radius);
            object-fit: cover;
            margin-right: var(--space-4);
            border: 1px solid var(--neutral-200);
        }
        
        .business-info {
            flex-grow: 1;
        }
        
        .business-name {
            font-weight: 600;
            font-size: 1.125rem;
            margin-bottom: var(--space-1);
            color: var(--neutral-900);
        }
        
        .business-category {
            font-size: 0.875rem;
            color: var(--neutral-600);
            margin-bottom: var(--space-2);
        }
        
        .business-meta {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        .business-body {
            padding: var(--space-5);
        }
        
        .business-section {
            margin-bottom: var(--space-5);
        }
        
        .business-section:last-child {
            margin-bottom: 0;
        }
        
        .business-section-title {
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--neutral-500);
            margin-bottom: var(--space-3);
        }
        
        .business-description {
            font-size: 0.875rem;
            color: var(--neutral-700);
            margin-bottom: var(--space-3);
        }
        
        .business-location {
            display: flex;
            align-items: center;
            gap: var(--space-2);
            font-size: 0.875rem;
            color: var(--neutral-700);
            margin-bottom: var(--space-2);
        }
        
        .business-hours {
            font-size: 0.875rem;
            color: var(--neutral-700);
        }
        
        .business-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--space-5);
            border-top: 1px solid var(--neutral-200);
        }
        
        .business-rating {
            display: flex;
            align-items: center;
            gap: var(--space-1);
            font-weight: 600;
            color: var(--neutral-900);
        }
        
        .business-rating-stars {
            color: var(--warning);
            letter-spacing: -0.25rem;
        }
        
        .business-reviews {
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        /* Notification items */
        .notification-item {
            display: flex;
            align-items: flex-start;
            padding: var(--space-4);
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-3);
            background: var(--neutral-50);
            transition: var(--transition-all);
            border-left: 3px solid transparent;
        }
        
        .notification-item.unread {
            background: rgba(58, 134, 255, 0.05);
            border-left-color: var(--primary);
        }
        
        .notification-item:hover {
            background: var(--neutral-100);
        }
        
        .notification-icon {
            flex-shrink: 0;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: var(--space-3);
            font-size: 1rem;
            color: white;
        }
        
        .notification-content {
            flex-grow: 1;
        }
        
        .notification-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--space-1);
        }
        
        .notification-title {
            font-weight: 500;
            color: var(--neutral-800);
            font-size: 0.875rem;
        }
        
        .notification-time {
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        .notification-body {
            font-size: 0.8125rem;
            color: var(--neutral-600);
            margin-bottom: var(--space-2);
        }
        
        .notification-footer {
            display: flex;
            gap: var(--space-2);
        }
        
        .notification-action {
            background: var(--primary);
            color: white;
            border: none;
            border-radius: var(--radius);
            font-size: 0.75rem;
            padding: var(--space-1) var(--space-3);
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-all);
        }
        
        .notification-action:hover {
            background: var(--primary-hover);
        }
        
        .notification-action.secondary {
            background: transparent;
            color: var(--neutral-700);
        }
        
        .notification-action.secondary:hover {
            background: var(--neutral-200);
        }
        
        /* Promotion card */
        .promotion-card {
            position: relative;
            background: white;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-md);
            overflow: hidden;
            transition: var(--transition-all);
            height: 100%;
        }
        
        .promotion-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .promotion-header {
            position: relative;
            padding: var(--space-5);
            background: var(--gradient-sunset);
            color: white;
        }
        
        .promotion-title {
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: var(--space-1);
        }
        
        .promotion-subtitle {
            font-size: 0.875rem;
            opacity: 0.9;
        }
        
        .promotion-offer {
            position: absolute;
            top: var(--space-4);
            right: var(--space-4);
            background: white;
            color: var(--neutral-900);
            border-radius: var(--radius-full);
            padding: var(--space-1) var(--space-3);
            font-weight: 600;
            font-size: 0.75rem;
        }
        
        .promotion-body {
            padding: var(--space-5);
        }
        
        .promotion-description {
            font-size: 0.875rem;
            color: var(--neutral-700);
            margin-bottom: var(--space-4);
        }
        
        .promotion-requirements {
            background: var(--neutral-50);
            border-radius: var(--radius-lg);
            padding: var(--space-3);
            font-size: 0.8125rem;
            color: var(--neutral-700);
            margin-bottom: var(--space-4);
        }
        
        .promotion-requirements-title {
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: var(--space-2);
            color: var(--neutral-900);
        }
        
        .promotion-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--space-5);
            padding-top: 0;
        }
        
        .promotion-meta {
            display: flex;
            flex-direction: column;
        }
        
        .promotion-expiry {
            font-size: 0.75rem;
            color: var(--neutral-500);
        }
        
        .promotion-claimed {
            font-size: 0.75rem;
            color: var(--primary);
            font-weight: 500;
        }
        
        /* Grid layouts */
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: var(--space-6);
        }
        
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-6);
        }
        
        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-6);
        }
        
        /* Animation classes */
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out forwards;
        }
        
        .animate-slide-up {
            animation: slideUp 0.5s ease-out forwards;
        }
        
        .animate-slide-left {
            animation: slideLeft 0.5s ease-out forwards;
        }
        
        .animate-pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        .animate-bounce {
            animation: bounce 1s ease infinite;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideLeft {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        /* Theming for dark mode */
        @media (prefers-color-scheme: dark) {
            /* We would add dark mode overrides here */
            /* This is just a placeholder for future dark mode support */
        }
        
        /* Responsive adjustments */
        @media screen and (max-width: 1200px) {
            .grid-4 {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        @media screen and (max-width: 992px) {
            .grid-3, .grid-4 {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media screen and (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 {
                grid-template-columns: 1fr;
            }
            
            .responsive-hide {
                display: none;
            }
        }
        
        /* Login/Signup page specific styles */
        .auth-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-lg);
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: var(--space-6);
        }
        
        .auth-logo {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: var(--space-1);
        }
        
        .auth-subtitle {
            font-size: 0.9rem;
            color: var(--neutral-600);
        }
        
        .auth-form-group {
            margin-bottom: var(--space-4);
        }
        
        .auth-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--neutral-700);
            margin-bottom: var(--space-2);
        }
        
        .auth-input {
            width: 100%;
            padding: var(--space-3);
            border: 1px solid var(--neutral-300);
            border-radius: var(--radius-lg);
            transition: var(--transition-all);
        }
        
        .auth-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(58, 134, 255, 0.1);
        }
        
        .auth-button {
            width: 100%;
            padding: var(--space-3);
            background: var(--primary);
            color: white;
            border: none;
            border-radius: var(--radius-lg);
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-all);
        }
        
        .auth-button:hover {
            background: var(--primary-hover);
        }
        
        .auth-separator {
            display: flex;
            align-items: center;
            text-align: center;
            margin: var(--space-4) 0;
            color: var(--neutral-500);
            font-size: 0.875rem;
        }
        
        .auth-separator::before,
        .auth-separator::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid var(--neutral-200);
        }
        
        .auth-separator::before {
            margin-right: var(--space-3);
        }
        
        .auth-separator::after {
            margin-left: var(--space-3);
        }
        
        .auth-footer {
            text-align: center;
            margin-top: var(--space-6);
            font-size: 0.875rem;
            color: var(--neutral-600);
        }
        
        .auth-link {
            color: var(--primary);
            font-weight: 500;
        }
        
        .auth-link:hover {
            text-decoration: underline;
        }
        
        /* Welcome landing specific styles */
        .welcome-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--space-6);
        }
        
        .welcome-hero {
            display: flex;
            align-items: center;
            margin-bottom: var(--space-16);
        }
        
        .welcome-content {
            flex: 1;
            padding-right: var(--space-10);
        }
        
        .welcome-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: var(--space-6);
            color: var(--neutral-900);
            line-height: 1.2;
        }
        
        .welcome-subtitle {
            font-size: 1.25rem;
            color: var(--neutral-600);
            margin-bottom: var(--space-6);
            line-height: 1.5;
        }
        
        .welcome-image {
            flex: 1;
        }
        
        .welcome-image img {
            max-width: 100%;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-xl);
        }
        
        .welcome-cta {
            display: flex;
            gap: var(--space-4);
        }
        
        .welcome-button {
            padding: var(--space-3) var(--space-6);
            border-radius: var(--radius-lg);
            font-weight: 500;
            transition: var(--transition-all);
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
        }
        
        .welcome-button-primary {
            background: var(--primary);
            color: white;
            border: none;
        }
        
        .welcome-button-primary:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .welcome-button-secondary {
            background: white;
            color: var(--primary);
            border: 1px solid var(--primary);
        }
        
        .welcome-button-secondary:hover {
            background: var(--neutral-50);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .welcome-features {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-8);
            margin-bottom: var(--space-16);
        }
        
        .feature-card {
            background: white;
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            box-shadow: var(--shadow-md);
            transition: var(--transition-all);
        }
        
        .feature-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .feature-icon {
            width: 48px;
            height: 48px;
            border-radius: var(--radius);
            background: var(--primary-light);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: var(--space-4);
        }
        
        .feature-title {
            font-weight: 600;
            font-size: 1.25rem;
            margin-bottom: var(--space-3);
            color: var(--neutral-900);
        }
        
        .feature-description {
            color: var(--neutral-700);
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

# ===== DATABASE STRUCTURES =====
DB_STRUCTURE = {
    "users": {
        "sample_user": {
            "user_id": "usr_123",
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "<hashed_password>",
            "account_type": "general",
            "verified": True,
            "joined_date": "2023-01-01",
            "interests": ["music", "tech"],
            "location": {"city": "New York", "lat": 40.7128, "lng": -74.0060}
        }
    },
    "businesses": {
        "sample_business": {
            "business_id": "biz_123",
            "owner_id": "usr_123",
            "business_name": "Cool Cafe",
            "category": "Food & Drink",
            "verified": False,
            "locations": [
                {"address": "123 Main St", "lat": 40.7128, "lng": -74.0060}
            ]
        }
    },
    "media": [
        {
            "media_id": "med_123",
            "user_id": "usr_123",
            "file_path": "media_gallery/usr_123_photo1.jpg",
            "location": {"name": "Central Park", "lat": 40.7829, "lng": -73.9654},
            "timestamp": "2023-01-01T12:00:00",
            "circle_id": "cir_123",
            "tags": ["nature", "park"],
            "reports": []
        }
    ],
    "circles": {
        "cir_123": {
            "circle_id": "cir_123",
            "name": "NYC Photographers",
            "description": "For photography enthusiasts in NYC",
            "type": "public",
            "location": {"city": "New York", "lat": 40.7128, "lng": -74.0060},
            "members": ["usr_123"],
            "events": ["evt_123"],
            "business_owned": False
        }
    },
    "events": {
        "evt_123": {
            "event_id": "evt_123",
            "circle_id": "cir_123",
            "name": "Sunset Photography Meetup",
            "description": "Let's capture the sunset together!",
            "location": {"name": "Brooklyn Bridge", "lat": 40.7061, "lng": -73.9969},
            "date": "2023-06-15",
            "time": "18:00",
            "organizer": "usr_123",
            "attendees": ["usr_123"],
            "capacity": 20,
            "tags": ["photography", "outdoors"]
        }
    },
    "promotions": {
        "promo_123": {
            "promo_id": "promo_123",
            "business_id": "biz_123",
            "offer": "20% off coffee",
            "requirements": "Post 3 photos with #CoolCafe",
            "start_date": "2023-01-01",
            "end_date": "2023-01-31",
            "claimed_by": ["usr_123"]
        }
    },
    "notifications": {
        "usr_123": [
            {
                "notification_id": "notif_123",
                "type": "event_reminder",
                "content": "Sunset Photography Meetup starts in 2 hours!",
                "timestamp": "2023-06-15T16:00:00",
                "read": False,
                "related_id": "evt_123"
            }
        ]
    },
    "reports": [
        {
            "report_id": "rep_123",
            "reporter_id": "usr_123",
            "content_id": "med_123",
            "content_type": "media",
            "reason": "Inappropriate content",
            "status": "pending",
            "timestamp": "2023-01-01T12:30:00"
        }
    ]
}

# ===== FILE PATHS =====
DB_FILES = {
    "users": "data/users.json",
    "businesses": "data/businesses.json",
    "media": "data/media.json",
    "circles": "data/circles.json",
    "events": "data/events.json",
    "promotions": "data/promotions.json",
    "notifications": "data/notifications.json",
    "reports": "data/reports.json"
}

MEDIA_DIR = "media_gallery"
os.makedirs("data", exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# ===== HELPER FUNCTIONS =====
def init_db():
    """Initialize database files with empty structures"""
    for file_path in DB_FILES.values():
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    for file_key, file_path in DB_FILES.items():
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({} if file_key in ["users", "businesses", "circles", "notifications"] else [], f)

def load_db(file_key):
    """Load database file"""
    try:
        with open(DB_FILES[file_key], "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty structure if file doesn't exist or is corrupted
        return {} if file_key in ["users", "businesses", "circles", "notifications"] else []

def save_db(file_key, data):
    """Save database file"""
    with open(DB_FILES[file_key], "w") as f:
        json.dump(data, f, indent=2)

def generate_id(prefix):
    """Generate unique ID"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def add_notification(user_id, notification_type, content, related_id=None):
    """Add notification to user's feed"""
    notifications = load_db("notifications")
    if user_id not in notifications:
        notifications[user_id] = []
    
    notifications[user_id].append({
        "notification_id": generate_id("notif"),
        "type": notification_type,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "read": False,
        "related_id": related_id
    })
    save_db("notifications", notifications)

def get_notification_icon(notification_type):
    """Get icon based on notification type"""
    icons = {
        "event_reminder": "📅",
        "event": "🎉",
        "circle": "👥",
        "promotion": "🎁",
        "login": "🔐",
        "media": "📸",
        "like": "❤️",
        "comment": "💬",
        "follow": "👋",
        "mention": "🔔",
    }
    return icons.get(notification_type, "🔔")

def get_initials(name):
    """Get initials from a name"""
    if not name:
        return "U"
    words = name.split()
    initials = "".join([word[0].upper() for word in words if word])
    return initials[:2]  # Return up to 2 initials

def get_avatar_color(name):
    """Generate a consistent color based on name"""
    colors = [
        "#3a86ff", "#4cc9f0", "#8338ec", "#ff006e", "#fb5607",
        "#ffbe0b", "#06d6a0", "#118ab2", "#073b4c", "#ef476f"
    ]
    
    color_seed = sum(ord(c) for c in name) if name else 0
    return colors[color_seed % len(colors)]

def create_user_avatar(name, size=150):
    """Create a colorful avatar with user's initials"""
    initials = get_initials(name)
    bg_color = get_avatar_color(name)
    
    # Create a BytesIO object
    img_io = BytesIO()
    # Create a new image with the color
    img = Image.new('RGB', (size, size), color=bg_color)
    # Get a drawing context
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font = ImageFont.truetype("arial.ttf", size=int(size/2))
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the text
    text_width, text_height = d.textsize(initials, font=font) if hasattr(d, 'textsize') else font.getsize(initials)
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)
    d.text(position, initials, fill="white", font=font)
    
    # Save the image to BytesIO object
    img.save(img_io, format='PNG')
    
    # Get the BytesIO value and encode as base64
    img_data = img_io.getvalue()
    return base64.b64encode(img_data).decode()

def format_date(date_str, format="%b %d, %Y"):
    """Format date string for display"""
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime(format)
    except:
        return date_str

def time_ago(date_str):
    """Convert date to 'time ago' format"""
    try:
        date_obj = datetime.fromisoformat(date_str)
        now = datetime.now()
        delta = now - date_obj
        
        if delta.days > 365:
            years = delta.days // 365
            return f"{years}y ago"
        elif delta.days > 30:
            months = delta.days // 30
            return f"{months}mo ago"
        elif delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        else:
            return "just now"
    except:
        return "unknown"

def get_random_placeholder_image(seed):
    """Get a random placeholder image URL with a seed for consistency"""
    return f"https://picsum.photos/seed/{seed}/800/600"

# Component rendering functions
def render_card(title, content, footer=None, badge=None, hover=True, premium=False):
    """Render a card with title and content"""
    if premium:
        card_html = f"""
        <div class="card-premium">
            <div class="card-premium-inner">
                <h3 class="card-title">{title}</h3>
                <div class="card-content">{content}</div>
                {f'<div class="card-footer">{footer}</div>' if footer else ''}
                {f'<div class="card-badge">{badge}</div>' if badge else ''}
            </div>
        </div>
        """
    else:
        hover_class = "card" if hover else "card" # No hover effect if hover=False
        card_html = f"""
        <div class="{hover_class}">
            <h3 class="card-title">{title}</h3>
            <div class="card-content">{content}</div>
            {f'<div class="card-footer">{footer}</div>' if footer else ''}
            {f'<div class="card-badge">{badge}</div>' if badge else ''}
        </div>
        """
    
    return card_html

def render_activity_item(user, action, time, icon="🔔", description=None):
    """Render an activity item"""
    return f"""
    <div class="activity-item">
        <div class="activity-icon">{icon}</div>
        <div class="activity-content">
            <div class="activity-header">
                <div class="activity-title">{user}</div>
                <div class="activity-time">{time}</div>
            </div>
            <div class="activity-description">{action}</div>
            {f'<div class="activity-meta">{description}</div>' if description else ''}
        </div>
    </div>
    """

def render_notification_item(notification):
    """Render a notification item"""
    notification_type = notification.get("type", "")
    content = notification.get("content", "")
    timestamp = notification.get("timestamp", "")
    read = notification.get("read", False)
    related_id = notification.get("related_id", "")
    
    icon = get_notification_icon(notification_type)
    time_str = time_ago(timestamp)
    
    unread_class = "unread" if not read else ""
    
    # Background color based on notification type
    bg_color = {
        "event_reminder": "#4cc9f0",
        "promotion": "#ff006e",
        "circle": "#3a86ff",
        "login": "#06d6a0",
    }.get(notification_type, "#8338ec")
    
    actions_html = ""
    if notification_type == "event_reminder":
        actions_html = """
        <div class="notification-footer">
            <button class="notification-action">View Event</button>
            <button class="notification-action secondary">Dismiss</button>
        </div>
        """
    elif notification_type == "promotion":
        actions_html = """
        <div class="notification-footer">
            <button class="notification-action">Claim Offer</button>
            <button class="notification-action secondary">Details</button>
        </div>
        """
    
    return f"""
    <div class="notification-item {unread_class}">
        <div class="notification-icon" style="background: {bg_color};">{icon}</div>
        <div class="notification-content">
            <div class="notification-header">
                <div class="notification-title">{notification_type.replace('_', ' ').title()}</div>
                <div class="notification-time">{time_str}</div>
            </div>
            <div class="notification-body">{content}</div>
            {actions_html}
        </div>
    </div>
    """

def render_stat_card(value, label, icon, change=None):
    """Render a statistics card"""
    change_html = ""
    if change is not None:
        change_class = "positive" if change >= 0 else "negative"
        change_arrow = "↑" if change >= 0 else "↓"
        change_html = f"""
        <div class="stat-change {change_class}">
            {change_arrow} {abs(change)}%
        </div>
        """
    
    return f"""
    <div class="stat-card">
        <div class="stat-icon">{icon}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
        {change_html}
    </div>
    """

def render_event_card(event, interactive=True):
    """Render an event card"""
    event_name = event.get("name", "Event")
    event_date = event.get("date", "")
    event_time = event.get("time", "")
    event_location = event.get("location", {}).get("name", "Location")
    event_circle = event.get("circle", "")
    event_description = event.get("description", "")
    event_attendees = event.get("attendees", [])
    event_capacity = event.get("capacity", 0)
    
    # Format date
    formatted_date = event_date if isinstance(event_date, str) else format_date(event_date)
    
    # Generate a seed for the placeholder image
    image_seed = sum(ord(c) for c in event_name) % 1000
    
    attendee_count = len(event_attendees) if isinstance(event_attendees, list) else event_attendees if isinstance(event_attendees, int) else 0
    
    buttons = ""
    if interactive:
        buttons = f"""
        <div style="display: flex; gap: 10px; margin-top: 10px;">
            <button class="stButton button">RSVP</button>
            <button class="stButton secondary-btn">Details</button>
        </div>
        """
    
    return f"""
    <div class="event-card">
        <div class="event-image">
            <img src="{get_random_placeholder_image(image_seed)}" alt="{event_name}">
            <div class="event-date-badge">{formatted_date}</div>
        </div>
        <div class="event-content">
            <div class="event-meta">
                <div class="event-category">{event_circle}</div>
                <div class="event-dot"></div>
                <div class="event-time">{event_time}</div>
            </div>
            <h3 class="event-title">{event_name}</h3>
            <div class="event-description">{event_description[:100]}{'...' if len(event_description) > 100 else ''}</div>
            <div class="event-footer">
                <div class="event-location">
                    📍 {event_location}
                </div>
                <div class="event-attendees">
                    {attendee_count} attending
                </div>
            </div>
        </div>
    </div>
    """

def render_circle_card(circle, interactive=True):
    """Render a circle card"""
    circle_name = circle.get("name", "Circle")
    circle_members = circle.get("members", [])
    circle_description = circle.get("description", "")
    circle_type = circle.get("type", "public")
    circle_tags = circle.get("tags", [])
    
    if isinstance(circle_members, list):
        member_count = len(circle_members)
    else:
        member_count = circle_members if isinstance(circle_members, int) else 0
    
    # Generate initials for the circle avatar
    initials = get_initials(circle_name)
    
    # Generate tags HTML
    tags_html = ""
    for tag in circle_tags[:3]:  # Limit to 3 tags for space
        tags_html += f'<div class="tag tag-primary">{tag}</div>'
    
    buttons = ""
    if interactive:
        buttons = f"""
        <button class="stButton button">Join Circle</button>
        """
    
    return f"""
    <div class="circle-card">
        <div class="circle-banner"></div>
        <div class="circle-avatar">{initials}</div>
        <div class="circle-content">
            <h3 class="circle-title">{circle_name}</h3>
            <div class="circle-description">{circle_description[:100]}{'...' if len(circle_description) > 100 else ''}</div>
            
            <div class="circle-stats">
                <div class="circle-stat">
                    <div class="circle-stat-value">{member_count}</div>
                    <div class="circle-stat-label">Members</div>
                </div>
                <div class="circle-stat">
                    <div class="circle-stat-value">5</div>
                    <div class="circle-stat-label">Events</div>
                </div>
                <div class="circle-stat">
                    <div class="circle-stat-value">12</div>
                    <div class="circle-stat-label">Posts</div>
                </div>
            </div>
            
            <div class="circle-tags">
                {tags_html}
                {f'<div class="tag">+{len(circle_tags) - 3} more</div>' if len(circle_tags) > 3 else ''}
            </div>
            
            <div class="circle-footer">
                <div class="circle-privacy">
                    {'🔒' if circle_type == 'private' else '🌐'} {circle_type.capitalize()}
                </div>
                {buttons}
            </div>
        </div>
    </div>
    """
        def render_business_card(business, interactive=True):
    """Render a business card"""
    business_name = business.get("business_name", "Business")
    business_category = business.get("category", "")
    business_description = business.get("description", "")
    business_verified = business.get("verified", False)
    business_locations = business.get("locations", [])
    
    # Get the first location
    location = business_locations[0].get("address", "") if business_locations else ""
    
    # Generate a seed for the placeholder logo
    logo_seed = sum(ord(c) for c in business_name) % 1000
    
    buttons = ""
    if interactive:
        buttons = f"""
        <button class="stButton button">Follow</button>
        """
    
    return f"""
    <div class="business-card">
        <div class="business-header">
            <img src="{get_random_placeholder_image(logo_seed)}" class="business-logo" alt="{business_name}">
            <div class="business-info">
                <h3 class="business-name">
                    {business_name}
                    {' <span style="color: #3a86ff; font-size: 0.8rem;">✓</span>' if business_verified else ''}
                </h3>
                <div class="business-category">{business_category}</div>
                <div class="business-meta">
                    <div>245 followers</div>
                    <div>•</div>
                    <div>56 mentions</div>
                </div>
            </div>
        </div>
        <div class="business-body">
            <div class="business-section">
                <div class="business-description">{business_description if business_description else 'No description available.'}</div>
            </div>
            <div class="business-section">
                <div class="business-section-title">Location</div>
                <div class="business-location">
                    📍 {location}
                </div>
            </div>
        </div>
        <div class="business-footer">
            <div class="business-rating">
                <div class="business-rating-stars">★★★★☆</div>
                <div>4.2</div>
            </div>
            <div class="business-reviews">36 reviews</div>
            {buttons}
        </div>
    </div>
    """

def render_promotion_card(promotion, interactive=True):
    """Render a promotion card"""
    promo_name = promotion.get("name", "Special Offer")
    promo_offer = promotion.get("offer", "")
    promo_description = promotion.get("description", "")
    promo_requirements = promotion.get("requirements", "")
    promo_start_date = promotion.get("start_date", "")
    promo_end_date = promotion.get("end_date", "")
    promo_claimed = len(promotion.get("claimed_by", [])) if isinstance(promotion.get("claimed_by", []), list) else 0
    
    # Format dates
    start_date_formatted = format_date(promo_start_date) if promo_start_date else ""
    end_date_formatted = format_date(promo_end_date) if promo_end_date else ""
    
    buttons = ""
    if interactive:
        buttons = f"""
        <button class="stButton button">Claim Offer</button>
        """
    
    return f"""
    <div class="promotion-card">
        <div class="promotion-header">
            <div class="promotion-title">{promo_name}</div>
            <div class="promotion-subtitle">Limited time offer</div>
            <div class="promotion-offer">{promo_offer}</div>
        </div>
        <div class="promotion-body">
            <div class="promotion-description">{promo_description if promo_description else 'Exclusive offer for Atmosphere users!'}</div>
            
            <div class="promotion-requirements">
                <div class="promotion-requirements-title">How to claim:</div>
                {promo_requirements}
            </div>
            
            <div class="promotion-footer">
                <div class="promotion-meta">
                    <div class="promotion-expiry">Valid until: {end_date_formatted}</div>
                    <div class="promotion-claimed">{promo_claimed} users claimed this offer</div>
                </div>
                {buttons}
            </div>
        </div>
    </div>
    """

def render_media_item(media_item, interactive=True):
    """Render a media gallery item"""
    media_id = media_item.get("media_id", "")
    location = media_item.get("location", {}).get("name", "")
    timestamp = media_item.get("timestamp", "")
    tags = media_item.get("tags", [])
    caption = media_item.get("caption", "")
    
    # Format time
    time_str = time_ago(timestamp)
    
    # Use file path or generate placeholder
    file_path = media_item.get("file_path", "")
    if file_path and os.path.exists(file_path):
        image_src = file_path
    else:
        image_seed = sum(ord(c) for c in media_id) % 1000 if media_id else random.randint(1, 1000)
        image_src = get_random_placeholder_image(image_seed)
    
    buttons = ""
    if interactive:
        buttons = f"""
        <div class="gallery-actions">
            <button>❤️</button>
            <button>💬</button>
            <button>🔗</button>
        </div>
        """
    
    return f"""
    <div class="gallery-item">
        <img src="{image_src}" class="gallery-image" alt="Media">
        <div class="gallery-overlay">
            <div class="gallery-title">{location}</div>
            <div class="gallery-meta">
                <div>{time_str}</div>
                <div>{', '.join(tags[:2])}{' +' + str(len(tags) - 2) if len(tags) > 2 else ''}</div>
            </div>
        </div>
    </div>
    """

def render_profile_card(user):
    """Render a user profile card"""
    user_id = user.get("user_id", "")
    full_name = user.get("full_name", "User")
    email = user.get("email", "")
    location = user.get("location", {}).get("city", "")
    interests = user.get("interests", [])
    joined_date = user.get("joined_date", "")
    account_type = user.get("account_type", "general")
    verified = user.get("verified", False)
    
    # Generate avatar
    avatar_data = create_user_avatar(full_name)
    
    # Format joined date
    joined_formatted = format_date(joined_date) if joined_date else ""
    
    # Create interests tags
    interests_html = ""
    for interest in interests[:3]:
        interests_html += f'<div class="tag tag-primary">{interest}</div>'
    
    if len(interests) > 3:
        interests_html += f'<div class="tag">+{len(interests) - 3} more</div>'
    
    return f"""
    <div class="profile-card">
        <img src="data:image/png;base64,{avatar_data}" class="profile-avatar" alt="{full_name}">
        <div class="profile-info">
            <div class="profile-name">
                {full_name}
                {' <span style="color: #3a86ff; font-size: 0.8rem;">✓</span>' if verified else ''}
            </div>
            <div class="profile-role">{account_type.capitalize()}</div>
            <div class="profile-meta">
                <div>📍 {location}</div>
                <div>•</div>
                <div>Joined {joined_formatted}</div>
            </div>
        </div>
    </div>
    """

def render_search_bar(placeholder="Search..."):
    """Render a styled search bar"""
    return f"""
    <div class="search-container">
        <div class="search-icon">🔍</div>
        <input type="text" class="search-input" placeholder="{placeholder}">
    </div>
    """

def render_badge(text, type="primary"):
    """Render a badge"""
    return f'<span class="badge badge-{type}">{text}</span>'

def render_toast(title, message, type="info"):
    """Render a toast notification"""
    icon = {
        "success": "✓",
        "error": "✕",
        "warning": "⚠",
        "info": "ℹ"
    }.get(type, "ℹ")
    
    return f"""
    <div class="toast toast-{type}">
        <div class="toast-icon">{icon}</div>
        <div class="toast-content">
            <div class="toast-title">{title}</div>
            <div class="toast-message">{message}</div>
        </div>
        <button class="toast-close">✕</button>
    </div>
    """

def render_timeline_item(title, date, content):
    """Render a timeline item"""
    return f"""
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-content">
            <div class="timeline-date">{date}</div>
            <div class="timeline-title">{title}</div>
            <div class="timeline-body">{content}</div>
        </div>
    </div>
    """

def render_welcome_banner(name):
    """Render a welcome banner"""
    current_time = datetime.now()
    greeting = "Good morning" if 5 <= current_time.hour < 12 else "Good afternoon" if 12 <= current_time.hour < 18 else "Good evening"
    
    return f"""
    <div class="card" style="background: var(--gradient-blue); color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="color: white; margin-bottom: 0.5rem;">{greeting}, {name.split()[0]}!</h2>
                <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 0;">Welcome back to your community. Discover what's happening today.</p>
            </div>
            <div style="font-size: 3rem;">👋</div>
        </div>
    </div>
    """

def render_modal(title, content, footer=None):
    """Render a modal dialog"""
    footer_html = f'<div class="modal-footer">{footer}</div>' if footer else ''
    
    return f"""
    <div class="modal-backdrop">
        <div class="modal">
            <div class="modal-header">
                <div class="modal-title">{title}</div>
                <button class="modal-close">✕</button>
            </div>
            <div class="modal-body">
                {content}
            </div>
            {footer_html}
        </div>
    </div>
    """

# ===== INITIALIZE DATABASES =====
init_db()
load_css()

# ===== AUTHENTICATION =====
def login():
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-hero">
            <div class="welcome-content">
                <h1 class="welcome-title">Connect with your community like never before</h1>
                <p class="welcome-subtitle">Atmosphere brings people together based on shared interests, locations, and experiences. Discover communities, events, and businesses around you.</p>
                <div class="welcome-cta">
                    <button class="welcome-button welcome-button-primary">Get Started</button>
                    <button class="welcome-button welcome-button-secondary">Learn More</button>
                </div>
            </div>
            <div class="welcome-image">
                <img src="https://images.unsplash.com/photo-1531545514256-b1400bc00f31?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80" alt="Community">
            </div>
        </div>
        
        <div class="welcome-features">
            <div class="feature-card">
                <div class="feature-icon">👥</div>
                <h3 class="feature-title">Connect with Circles</h3>
                <p class="feature-description">Join communities based on your interests, hobbies, or location. Engage with like-minded people and build meaningful connections.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📅</div>
                <h3 class="feature-title">Discover Events</h3>
                <p class="feature-description">Find local events happening around you. From workshops to meetups, never miss out on experiences that matter to you.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏬</div>
                <h3 class="feature-title">Support Local Businesses</h3>
                <p class="feature-description">Discover and support local businesses. Claim exclusive offers and promotions when you engage with their community.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-header">
                <div class="auth-logo">🌍 Atmosphere</div>
                <div class="auth-subtitle">Sign in to your account</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if login_button:
                if login_user(username, password):
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    st.experimental_rerun()
        
        st.markdown("""
            <div class="auth-separator">OR</div>
            
            <button class="auth-button" style="background: #4285F4; margin-bottom: 10px;">
                Continue with Google
            </button>
            
            <button class="auth-button" style="background: #3b5998; margin-bottom: 20px;">
                Continue with Facebook
            </button>
            
            <div class="auth-footer">
                Don't have an account? <a href="#" class="auth-link">Sign up</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def login_user(username, password):
    if not username or not password:
        st.error("Please enter both username and password")
        return False

    users = load_db("users")
    if username in users and verify_password(password, users[username]["password"]):
        st.session_state["user"] = users[username]
        st.session_state["logged_in"] = True
        add_notification(users[username]["user_id"], "login", "Welcome back to Atmosphere!")
        return True
    else:
        st.error("Invalid username or password")
        return False

def signup():
    st.markdown('<div class="auth-container" style="max-width: 800px;">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="auth-header">
            <div class="auth-logo">🌍 Atmosphere</div>
            <div class="auth-subtitle">Create your account</div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["General User", "Business Account"])
    
    with tab1:
        with st.form("general_signup"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", placeholder="Enter your full name")
            with col2:
                username = st.text_input("Username", placeholder="Choose a username")
            
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email", placeholder="Enter your email")
            with col2:
                location = st.text_input("Your Location", placeholder="City, Country")
                
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password", type="password", placeholder="Create a password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
            interests = st.multiselect("Your Interests", 
                                     ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Fashion", "Books", "Movies"])
            
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                signup_btn = st.form_submit_button("Create Account", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True, 
                                     on_click=lambda: setattr(st.session_state, "auth_page", "login"))
            
            if signup_btn:
                if not all([full_name, username, email, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif not terms:
                    st.error("You must agree to the Terms of Service and Privacy Policy")
                elif password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    users = load_db("users")
                    if username in users:
                        st.error("Username already exists!")
                    else:
                        user_id = generate_id("usr")
                        users[username] = {
                            "user_id": user_id,
                            "full_name": full_name,
                            "email": email,
                            "password": hash_password(password),
                            "account_type": "general",
                            "verified": False,
                            "joined_date": datetime.now().isoformat(),
                            "interests": interests,
                            "location": {"city": location}
                        }
                        save_db("users", users)
                        st.session_state["user"] = users[username]
                        st.session_state["logged_in"] = True
                        
                        # Add welcome notification
                        add_notification(user_id, "login", f"Welcome to Atmosphere, {full_name}! Complete your profile to get started.")
                        
                        st.success("Account created successfully!")
                        st.balloons()
                        time.sleep(1)
                        st.experimental_rerun()

    with tab2:
        with st.form("business_signup"):
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("Business Name", placeholder="Enter your business name")
            with col2:
                category = st.selectbox("Business Category", 
                                      ["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"])
            
            col1, col2 = st.columns(2)
            with col1:
                owner_name = st.text_input("Owner/Representative Name", placeholder="Your full name")
            with col2:
                username = st.text_input("Username", placeholder="Choose a username")
                
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Business Email", placeholder="Enter business email")
            with col2:
                address = st.text_input("Business Address", placeholder="Full business address")
                
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password", type="password", placeholder="Create a password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            business_description = st.text_area("Business Description", placeholder="Tell people about your business", height=100)
            
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                signup_btn = st.form_submit_button("Register Business", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True, 
                                     on_click=lambda: setattr(st.session_state, "auth_page", "login"))
            
            if signup_btn:
                if not all([business_name, owner_name, username, email, password, confirm_password, address]):
                    st.error("Please fill in all required fields")
                elif not terms:
                    st.error("You must agree to the Terms of Service and Privacy Policy")
                elif password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    users = load_db("users")
                    businesses = load_db("businesses")
                    
                    if username in users:
                        st.error("Username already exists!")
                    else:
                        # Create user account
                        user_id = generate_id("usr")
                        users[username] = {
                            "user_id": user_id,
                            "full_name": owner_name,
                            "email": email,
                            "password": hash_password(password),
                            "account_type": "business",
                            "verified": False,
                            "joined_date": datetime.now().isoformat()
                        }
                        
                        # Create business profile
                        business_id = generate_id("biz")
                        businesses[business_id] = {
                            "business_id": business_id,
                            "owner_id": user_id,
                            "business_name": business_name,
                            "category": category,
                            "verified": False,
                            "description": business_description,
                            "locations": [{"address": address}]
                        }
                        
                        save_db("users", users)
                        save_db("businesses", businesses)
                        st.session_state["user"] = users[username]
                        st.session_state["business"] = businesses[business_id]
                        st.session_state["logged_in"] = True
                        
                        # Add welcome notification
                        add_notification(user_id, "login", f"Welcome to Atmosphere! Complete your business profile to get started.")
                        
                        st.success("Business account created! Verification pending.")
                        st.balloons()
                        time.sleep(1)
                        st.experimental_rerun()
    
    st.markdown("""
        <div class="auth-footer">
            Already have an account? <a href="#" class="auth-link">Sign in</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== MAIN APP PAGES =====
def home_page():
    st.markdown(render_welcome_banner(st.session_state['user']['full_name']), unsafe_allow_html=True)
    
    # Recent notifications
    notifications = load_db("notifications").get(st.session_state["user"]["user_id"], [])
    unread_count = sum(1 for n in notifications if not n.get("read", False))
    
    if unread_count > 0:
        st.markdown(f"""
        <div class="card" style="margin-bottom: 20px; background-color: rgba(58, 134, 255, 0.05); border-left: 3px solid var(--primary);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="margin-bottom: 5px;">You have {unread_count} unread notification{'s' if unread_count > 1 else ''}</h3>
                    <p style="margin: 0;">Check your notifications to stay updated with your circles and events.</p>
                </div>
                <button class="stButton button">View Notifications</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # User stats
    st.markdown("## Your Activity")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_stat_card("5", "Circles Joined", "👥", change=10), unsafe_allow_html=True)
    with col2:
        st.markdown(render_stat_card("3", "Events Attended", "📅", change=0), unsafe_allow_html=True)
    with col3:
        st.markdown(render_stat_card("12", "Media Shared", "📸", change=20), unsafe_allow_html=True)
    with col4:
        st.markdown(render_stat_card("28", "Connections", "🔗", change=5), unsafe_allow_html=True)
    
    # Activity feed and upcoming events
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Activity Feed")
        tab1, tab2 = st.tabs(["All Activity", "Your Circles"])
        
        with tab1:
            # Sample activity data
            activities = [
                {"user": "JaneDoe", "action": "posted a photo in NYC Photographers", "time": "2h ago", "icon": "📸"},
                {"user": "MikeT", "action": "created an event: Central Park Picnic", "time": "5h ago", "icon": "📅"},
                {"user": "CoffeeShop", "action": "offered a new promotion: 20% off for members", "time": "1d ago", "icon": "🎁"},
                {"user": "Sarah", "action": "joined your Photography circle", "time": "1d ago", "icon": "👥"},
                {"user": "TechGroup", "action": "posted about an upcoming hackathon", "time": "2d ago", "icon": "💻"}
            ]
            
            for activity in activities:
                st.markdown(render_activity_item(
                    activity['user'], 
                    activity['action'], 
                    activity['time'],
                    activity['icon']
                ), unsafe_allow_html=True)
            
            if st.button("Load More Activities", use_container_width=True):
                st.info("Loading more activities...")
        
        with tab2:
            circles = [
                {"name": "NYC Photographers", "members": 45, "description": "Photography enthusiasts in New York", "new_posts": 3},
                {"name": "Food Lovers", "members": 120, "description": "Discovering the best food spots", "new_posts": 7},
                {"name": "Tech Enthusiasts", "members": 89, "description": "Discussing tech innovations", "new_posts": 2}
            ]
            
            for circle in circles:
                with st.expander(f"{circle['name']} • {circle['members']} members • {circle['new_posts']} new posts"):
                    st.write(circle['description'])
                    
                    # Recent posts
                    st.markdown("#### Recent Posts")
                    
                    # Sample posts for this circle
                    posts = [
                        {"user": f"User{i}", "content": f"Sample post content for {circle['name']}", "time": f"{i}h ago"}
                        for i in range(1, 4)
                    ]
                    
                    for post in posts:
                        st.markdown(f"""
                        <div style="background: var(--neutral-50); padding: 15px; border-radius: var(--radius-lg); margin-bottom: 10px;">
                            <div style="font-weight: 600; margin-bottom: 5px;">{post['user']}</div>
                            <div style="margin-bottom: 5px;">{post['content']}</div>
                            <div style="color: var(--neutral-500); font-size: 0.8rem;">{post['time']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Post form
                    st.text_area("Write a post", placeholder="Share something with this circle...", key=f"post_{circle['name']}")
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.button("Add Media", key=f"media_{circle['name']}")
                    with col2:
                        st.button("Post", key=f"submit_{circle['name']}", use_container_width=True)
    
    with col2:
        st.markdown("## Upcoming Events")
        
        # Sample events
        events = [
            {"name": "Sunset Photography", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
            {"name": "Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown", "circle": "Food Lovers", "description": "Explore various cuisines and dishes at the annual food festival."},
            {"name": "Tech Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Innovation Center", "circle": "Tech Enthusiasts", "description": "Network with tech professionals and learn about the latest innovations."}
        ]
        
        for event in events:
            st.markdown(render_event_card(event), unsafe_allow_html=True)
        
        if st.button("View All Events", use_container_width=True):
            st.session_state["page"] = "events"
            st.experimental_rerun()
    
    # Suggested circles
    st.markdown("## Suggested For You")
    
    col1, col2, col3 = st.columns(3)
    
    circles = [
        {"name": "NYC Photographers", "members": 245, "description": "For photography enthusiasts in NYC", "tags": ["Photography", "Art", "NYC"]},
        {"name": "Tech Innovators", "members": 189, "description": "Discuss the latest in technology", "tags": ["Technology", "Innovation", "Coding"]},
        {"name": "Foodies United", "members": 320, "description": "Discover and share great food spots", "tags": ["Food", "Restaurants", "Cooking"]}
    ]
    
    with col1:
        st.markdown(render_circle_card(circles[0]), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_circle_card(circles[1]), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_circle_card(circles[2]), unsafe_allow_html=True)
    
    if st.button("Discover More Circles", use_container_width=True):
        st.session_state["page"] = "circles"
        st.experimental_rerun()

def explore_page():
    st.markdown("## 🔍 Explore")
    
    # Search and filters
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.markdown(render_search_bar("Search for circles, events, or locations"), unsafe_allow_html=True)
    with col2:
        st.multiselect("Filter by", ["Circles", "Events", "Users", "Businesses", "Media"])
    with col3:
        st.selectbox("Sort by", ["Recent", "Popular", "Nearby"])
    
    # Map view
    st.markdown("## 📍 Discover Around You")
    
    # Interactive map placeholder
    st.markdown("""
    <div style="position: relative; border-radius: var(--radius-xl); overflow: hidden; margin-bottom: 20px; box-shadow: var(--shadow-lg); height: 400px;">
        <img src="https://maps.googleapis.com/maps/api/staticmap?center=40.7128,-74.0060&zoom=12&size=1200x400&style=feature:water|color:0x4361ee&style=feature:road|color:0xffffff&style=element:labels|visibility:off&style=feature:poi|visibility:off&key=YOUR_API_KEY" style="width: 100%; height: 100%; object-fit: cover;">
        <div style="position: absolute; top: 20px; left: 20px; background: white; padding: 10px 20px; border-radius: var(--radius-full); box-shadow: var(--shadow);">
            <span style="font-weight: 600; color: var(--neutral-900);">New York City</span>
        </div>
        <div style="position: absolute; bottom: 20px; right: 20px; display: flex; gap: 10px;">
            <button style="background: white; border: none; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow);">
                <span style="font-size: 20px;">+</span>
            </button>
            <button style="background: white; border: none; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow);">
                <span style="font-size: 20px;">-</span>
            </button>
        </div>
        
        <!-- Map markers -->
        <div style="position: absolute; top: 40%; left: 30%;">
            <div class="map-marker">
                <div class="map-marker-content">12</div>
            </div>
        </div>
        <div style="position: absolute; top: 60%; left: 50%;">
            <div class="map-marker">
                <div class="map-marker-content">8</div>
            </div>
        </div>
        <div style="position: absolute; top: 30%; left: 70%;">
            <div class="map-marker">
                <div class="map-marker-content">5</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        # Featured sections with tabs
    st.markdown("## Trending Near You")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Circles", "Events", "Places", "People"])
    
    with tab1:
        st.markdown("### Popular Circles")
        col1, col2, col3 = st.columns(3)
        
        circles = [
            {"name": "NYC Photographers", "members": 245, "description": "For photography enthusiasts in NYC", "tags": ["Photography", "Art", "NYC"]},
            {"name": "Tech Innovators", "members": 189, "description": "Discuss the latest in technology", "tags": ["Technology", "Innovation", "Coding"]},
            {"name": "Foodies United", "members": 320, "description": "Discover and share great food spots", "tags": ["Food", "Restaurants", "Cooking"]},
            {"name": "Outdoor Adventures", "members": 156, "description": "Explore the great outdoors together", "tags": ["Nature", "Hiking", "Adventure"]},
            {"name": "Book Club NYC", "members": 112, "description": "Monthly book discussions and recommendations", "tags": ["Books", "Reading", "Literature"]},
            {"name": "Fitness Enthusiasts", "members": 278, "description": "Workouts, nutrition tips, and wellness", "tags": ["Fitness", "Health", "Wellness"]}
        ]
        
        for i, col in enumerate([col1, col2, col3]):
            with col:
                st.markdown(render_circle_card(circles[i]), unsafe_allow_html=True)
        
        for i, col in enumerate([col1, col2, col3]):
            with col:
                st.markdown(render_circle_card(circles[i+3]), unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Upcoming Events")
        col1, col2 = st.columns(2)
        events = [
            {"name": "Sunset Photography", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
            {"name": "Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown", "circle": "Food Lovers", "description": "Explore various cuisines and dishes at the annual food festival."},
            {"name": "Tech Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Innovation Center", "circle": "Tech Enthusiasts", "description": "Network with tech professionals and learn about the latest innovations."},
            {"name": "Morning Yoga", "date": "Jun 18", "time": "8:00 AM", "location": "Central Park", "circle": "Fitness Enthusiasts", "description": "Start your day with energizing yoga in the park."}
        ]
        
        with col1:
            st.markdown(render_event_card(events[0]), unsafe_allow_html=True)
            st.markdown(render_event_card(events[2]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_event_card(events[1]), unsafe_allow_html=True)
            st.markdown(render_event_card(events[3]), unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Popular Places")
        col1, col2, col3 = st.columns(3)
        
        businesses = [
            {"business_name": "Cool Cafe", "category": "Food & Drink", "locations": [{"address": "123 Main St, New York"}], "verified": True, "description": "Cozy cafe with great coffee and pastries."},
            {"business_name": "Tech Hub", "category": "Workspace", "locations": [{"address": "456 Tech Ave, New York"}], "verified": True, "description": "Modern coworking space for tech professionals."},
            {"business_name": "Green Park Restaurant", "category": "Food & Drink", "locations": [{"address": "789 Park Rd, New York"}], "verified": False, "description": "Farm-to-table dining with seasonal ingredients."}
        ]
        
        with col1:
            st.markdown(render_business_card(businesses[0]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_business_card(businesses[1]), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_business_card(businesses[2]), unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### People to Follow")
        col1, col2, col3, col4 = st.columns(4)
        
        users = [
            {"user_id": "usr_1", "full_name": "Jane Smith", "account_type": "photographer", "location": {"city": "New York"}, "joined_date": "2023-01-01", "verified": True},
            {"user_id": "usr_2", "full_name": "Alex Johnson", "account_type": "event_organizer", "location": {"city": "Brooklyn"}, "joined_date": "2023-02-15", "verified": False},
            {"user_id": "usr_3", "full_name": "Maria Garcia", "account_type": "food_blogger", "location": {"city": "Queens"}, "joined_date": "2023-03-10", "verified": True},
            {"user_id": "usr_4", "full_name": "David Kim", "account_type": "tech_expert", "location": {"city": "Manhattan"}, "joined_date": "2023-01-20", "verified": False}
        ]
        
        with col1:
            st.markdown(render_profile_card(users[0]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_profile_card(users[1]), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_profile_card(users[2]), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_profile_card(users[3]), unsafe_allow_html=True)
    
    # Popular hashtags
    st.markdown("### 🔖 Trending Topics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    hashtags = ["#Photography", "#FoodFestNYC", "#TechTalks", "#SummerVibes", "#CentralPark"]
    
    for i, (col, tag) in enumerate(zip([col1, col2, col3, col4, col5], hashtags)):
        with col:
            if st.button(tag, key=f"tag_{i}", use_container_width=True):
                st.session_state["search_query"] = tag
                st.experimental_rerun()
    
    # Featured promotions
    st.markdown("## Special Offers")
    col1, col2, col3 = st.columns(3)
    
    promotions = [
        {"name": "Summer Special", "offer": "20% off all items", "description": "Enjoy summer savings on all menu items. Limited time only!", "requirements": "Show this offer to the cashier when ordering.", "start_date": "2023-06-01", "end_date": "2023-08-31", "claimed_by": ["usr_1", "usr_2", "usr_3"]},
        {"name": "Photo Contest", "offer": "Win a free camera", "description": "Submit your best photos for a chance to win a professional camera.", "requirements": "Post 3 photos with #PhotoContest and tag our business.", "start_date": "2023-06-15", "end_date": "2023-07-15", "claimed_by": ["usr_1"]},
        {"name": "First-Time Customer", "offer": "Free dessert", "description": "New customers get a free dessert with any meal purchase.", "requirements": "Mention this offer when ordering. First-time customers only.", "start_date": "2023-06-01", "end_date": "2023-12-31", "claimed_by": ["usr_1", "usr_2"]}
    ]
    
    with col1:
        st.markdown(render_promotion_card(promotions[0]), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_promotion_card(promotions[1]), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_promotion_card(promotions[2]), unsafe_allow_html=True)

def media_page():
    st.markdown("## 📸 Media Gallery")
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["Your Gallery", "Upload Media", "Discover"])
    
    with tab1:
        st.markdown("### Your Photos & Videos")
        
        # Filter and sort options
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Filter by", ["All Media", "Photos", "Videos", "Tagged", "Archived"])
        with col2:
            st.selectbox("Circle", ["All Circles", "NYC Photographers", "Food Lovers", "Tech Enthusiasts"])
        with col3:
            st.selectbox("Sort by", ["Newest", "Oldest", "Most Liked", "Most Commented"])
        
        # Gallery view
        media_items = [
            {"media_id": f"med_{i}", "location": {"name": f"Location {i}"}, "timestamp": (datetime.now() - timedelta(days=i)).isoformat(), "tags": ["nature", "city", "art"][:i%3+1]}
            for i in range(1, 10)
        ]
        
        st.markdown('<div class="gallery-container">', unsafe_allow_html=True)
        
        for item in media_items:
            st.markdown(render_media_item(item), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Load More", use_container_width=True):
            st.info("Loading more media...")
    
    with tab2:
        st.markdown("### Share Your Moments")
        
        # Upload options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Camera capture with stylish container
            st.markdown("""
            <div style="border: 2px dashed var(--primary); border-radius: var(--radius-xl); padding: 20px; text-align: center; margin-bottom: 20px;">
                <div style="color: var(--primary); font-size: 1.2rem; margin-bottom: 10px;">📸 Take a photo or upload</div>
            </div>
            """, unsafe_allow_html=True)
            captured_photo = st.camera_input("", label_visibility="collapsed")
            
            # Alternative upload
            uploaded_file = st.file_uploader("Or upload from your device", type=["jpg", "jpeg", "png", "mp4"], label_visibility="collapsed")
        
        with col2:
            # Media details
            st.text_input("Caption", placeholder="Write a caption...")
            location = st.text_input("Location", placeholder="Add a location")
            
            # Circle selection
            circles = ["", "NYC Photographers", "Food Lovers", "Tech Enthusiasts", "Travel Enthusiasts"]
            selected_circle = st.selectbox("Share to Circle", circles)
            
            # Privacy
            privacy = st.radio("Privacy Setting", ["Public", "Circle Members Only", "Private"])
            
            # Tags
            tags = st.multiselect("Add Tags", ["Nature", "Food", "Tech", "Art", "Sports", "Travel", "Portrait", "Friends", "Family"])
        
        # Upload button
        if st.button("Share Now", use_container_width=True, type="primary") and (captured_photo or uploaded_file):
            # Process media upload
            media_source = captured_photo if captured_photo else uploaded_file
            
            # Save media
            media_id = generate_id("med")
            filename = f"{st.session_state['user']['user_id']}_{media_id}.jpg"
            filepath = os.path.join(MEDIA_DIR, filename)
            
            try:
                image = Image.open(media_source)
                image.save(filepath)
                
                # Add to database
                media = load_db("media")
                media.append({
                    "media_id": media_id,
                    "user_id": st.session_state["user"]["user_id"],
                    "file_path": filepath,
                    "location": {"name": location} if location else None,
                    "caption": st.session_state.get("caption", ""),
                    "timestamp": datetime.now().isoformat(),
                    "circle_id": selected_circle if selected_circle else None,
                    "privacy": privacy.lower(),
                    "tags": tags,
                    "likes": 0,
                    "comments": [],
                    "reports": []
                })
                save_db("media", media)
                
                st.success("Media shared successfully!")
                
                # Add notification for circle members if shared to a circle
                if selected_circle:
                    # In a real app, you'd notify circle members
                    pass
                
                # Check if this qualifies for any promotions
                promotions = load_db("promotions")
                for promo_id, promo in promotions.items():
                    if any(tag.lower() in [t.lower() for t in tags] for tag in promo.get("tags", [])):
                        add_notification(st.session_state["user"]["user_id"], "promotion", 
                                        f"Your photo qualifies for {promo['offer']} from {promo_id}!")
            except Exception as e:
                st.error(f"Error saving media: {str(e)}")
    
    with tab3:
        st.markdown("### Discover Photos")
        
        # Filter by categories
        st.markdown("""
        <div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px 0; margin-bottom: 20px;">
            <div style="background: var(--primary); color: white; padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">All</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Nature</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Urban</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">People</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Food</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Art</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Technology</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Travel</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Masonry gallery layout
        st.markdown("""
        <div style="columns: 4 200px; column-gap: 16px;">
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682685797898-6d7587974771?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682687982501-1e58ab814714?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682687220063-4742bd7fd538?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682686581776-b62f563de74f?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682687220067-dced9a881b56?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682687220123-2a3473130a9d?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682685797828-d3b2561deef4?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682686580391-8b2263139d7a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px;">
                <img src="https://images.unsplash.com/photo-1682685797365-41f45b562c0a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Explore More", use_container_width=True):
            st.info("Loading more media...")

def circles_page():
    st.markdown("## 👥 Circles")
    
    tab1, tab2, tab3 = st.tabs(["Your Circles", "Discover", "Create Circle"])
    
    with tab1:
        st.markdown("### Your Circle Communities")
        
        # Sample data - in real app would load from DB
        user_circles = [
            {
                "name": "NYC Photographers", 
                "members": 45, 
                "unread": 3, 
                "description": "For photography enthusiasts in NYC",
                "tags": ["Photography", "Art", "NYC"],
                "type": "public",
                "recent_posts": [
                    {"user": "JaneDoe", "content": "Great sunset shots at Brooklyn Bridge today!", "time": "2h ago"},
                    {"user": "MarkT", "content": "Anyone interested in a Central Park photowalk this Saturday?", "time": "5h ago"}
                ]
            },
            {
                "name": "Food Lovers", 
                "members": 120, 
                "unread": 7,
                "description": "Discovering and sharing great food spots",
                "tags": ["Food", "Restaurants", "Cooking"],
                "type": "public",
                "recent_posts": [
                    {"user": "FoodieChef", "content": "Just tried that new Italian place downtown. Amazing pasta!", "time": "1h ago"},
                    {"user": "TasteHunter", "content": "Check out my review of the top 5 burger joints in the city", "time": "1d ago"}
                ]
            },
            {
                "name": "Tech Enthusiasts", 
                "members": 89, 
                "unread": 2,
                "description": "Discussing tech innovations",
                "tags": ["Technology", "Coding", "Innovation"],
                "type": "private",
                "recent_posts": [
                    {"user": "TechGuru", "content": "Here's my review of the latest smartphone release", "time": "3h ago"},
                    {"user": "CodeMaster", "content": "Anyone attending the developer conference next month?", "time": "1d ago"}
                ]
            }
        ]
        
        # Display in grid layout
        cols = st.columns(3)
        
        for i, circle in enumerate(user_circles):
            with cols[i % 3]:
                st.markdown(render_circle_card(circle, interactive=False), unsafe_allow_html=True)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.button("View Circle", key=f"view_{circle['name']}", use_container_width=True)
                with col2:
                    st.button("See Events", key=f"events_{circle['name']}", use_container_width=True)
        
        st.markdown("### Circle Activity")
        
        # Display activities for the first circle (as an example)
        if user_circles:
            circle = user_circles[0]
            st.markdown(f"#### Recent in {circle['name']}")
            
            st.markdown('<div class="timeline">', unsafe_allow_html=True)
            
            timeline_items = [
                {"title": "New Photo Album", "date": "2 hours ago", "content": "Jane uploaded 12 new photos from the Brooklyn Bridge photoshoot."},
                {"title": "Upcoming Event", "date": "5 hours ago", "content": "Mark created a new event: Central Park Photowalk on Saturday at 4pm."},
                {"title": "Circle Discussion", "date": "1 day ago", "content": "12 members are discussing the best camera settings for night photography."}
            ]
            
            for item in timeline_items:
                st.markdown(render_timeline_item(item["title"], item["date"], item["content"]), unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Discover New Circles")
        
        # Search and filters
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(render_search_bar("Search circles by name, interest, or location"), unsafe_allow_html=True)
        with col2:
            st.selectbox("Sort by", ["Popular", "New", "Active", "Nearby"])
        
        # Categories quick filter
        st.markdown("""
        <div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px 0; margin-bottom: 20px;">
            <div style="background: var(--primary); color: white; padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">All Categories</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Photography</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Food</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Technology</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Sports</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Art</div>
            <div style="background: var(--neutral-100); color: var(--neutral-700); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Music</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample circles
        circles = [
            {"name": "Tech Innovators", "members": 189, "description": "Discuss the latest in technology", "tags": ["Technology", "Gadgets", "Innovation"], "type": "public"},
            {"name": "Fitness Community", "members": 87, "description": "Share workout tips and meetups", "tags": ["Fitness", "Health", "Wellness"], "type": "public"},
            {"name": "Art Lovers", "members": 142, "description": "Appreciate and create art together", "tags": ["Art", "Creativity", "Museums"], "type": "public"},
            {"name": "Book Club", "members": 56, "description": "Discuss and recommend great reads", "tags": ["Books", "Reading", "Literature"], "type": "private"},
            {"name": "Travel Adventures", "members": 210, "description": "Share travel experiences and tips", "tags": ["Travel", "Adventure", "Photography"], "type": "public"},
            {"name": "Music Enthusiasts", "members": 175, "description": "For those who love music of all genres", "tags": ["Music", "Concerts", "Instruments"], "type": "public"}
        ]
        
        # Display in grid layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(render_circle_card(circles[0]), unsafe_allow_html=True)
            st.markdown(render_circle_card(circles[3]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_circle_card(circles[1]), unsafe_allow_html=True)
            st.markdown(render_circle_card(circles[4]), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_circle_card(circles[2]), unsafe_allow_html=True)
            st.markdown(render_circle_card(circles[5]), unsafe_allow_html=True)
        
        if st.button("Discover More Circles", use_container_width=True):
            st.info("Finding more circles for you...")
    
    with tab3:
        st.markdown("### Create a New Circle")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("create_circle"):
                # Circle details
                st.markdown("#### Basic Information")
                name = st.text_input("Circle Name", placeholder="Give your circle a catchy name")
                description = st.text_area("Description", placeholder="What's your circle about?", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    circle_type = st.radio("Privacy Type", ["Public", "Private"])
                with col2:
                    location = st.text_input("Primary Location", placeholder="City, Country (optional)")
                
                # Additional settings
                st.markdown("#### Circle Settings")
                col1, col2 = st.columns(2)
                with col1:
                    join_approval = st.checkbox("Require approval for new members")
                with col2:
                    post_approval = st.checkbox("Require approval for posts")
                
                # Tags
                tags = st.multiselect("Tags (helps people find your circle)", 
                                    ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography", "Books", "Movies", "Fashion", "Education"])
                
                # Cover image
                st.markdown("#### Circle Image")
                cover_image = st.file_uploader("Upload a cover image (optional)", type=["jpg", "jpeg", "png"])
                
                # Submit
                col1, col2 = st.columns(2)
                with col1:
                    submit_button = st.form_submit_button("Create Circle", use_container_width=True)
                with col2:
                    cancel_button = st.form_submit_button("Cancel", use_container_width=True)
                
                if submit_button:
                    if not name:
                        st.error("Please provide a name for your circle")
                    else:
                        circle_id = generate_id("cir")
                        circles = load_db("circles")
                        circles[circle_id] = {
                            "circle_id": circle_id,
                            "name": name,
                            "description": description,
                            "type": circle_type.lower(),
                            "creator": st.session_state["user"]["user_id"],
                            "members": [st.session_state["user"]["user_id"]],
                            "location": {"name": location} if location else None,
                            "join_approval": join_approval,
                            "post_approval": post_approval,
                            "tags": tags,
                            "created_at": datetime.now().isoformat()
                        }
                        save_db("circles", circles)
                        
                        # Save cover image if provided
                        if cover_image:
                            image_path = f"media_gallery/circle_{circle_id}_cover.jpg"
                            Image.open(cover_image).save(image_path)
                            circles[circle_id]["cover_image"] = image_path
                            save_db("circles", circles)
                        
                        st.success(f"Circle '{name}' created successfully!")
                        add_notification(st.session_state["user"]["user_id"], "circle", f"You created a new circle: {name}")
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3 class="card-title">Circle Guidelines</h3>
                <div class="card-content">
                    <p><strong>What makes a great circle?</strong></p>
                    <ul>
                        <li>Clear purpose and description</li>
                        <li>Relevant tags to help people find it</li>
                        <li>Regular engagement and activities</li>
                        <li>Welcoming environment for all members</li>
                    </ul>
                    <p><strong>As a circle creator, you can:</strong></p>
                    <ul>
                        <li>Organize events for your members</li>
                        <li>Create discussion topics</li>
                        <li>Moderate content and members</li>
                        <li>Customize circle settings and appearance</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        def events_page():
    st.markdown("## 📅 Events")
    
    tab1, tab2, tab3 = st.tabs(["Discover Events", "Your Events", "Create Event"])
    
    with tab1:
        st.markdown("### Find Events Near You")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            date_filter = st.selectbox("When", ["Any time", "Today", "This weekend", "Next week", "Next month"])
        with col2:
            category_filter = st.selectbox("Category", ["All categories", "Photography", "Food", "Technology", "Arts", "Outdoors", "Sports"])
        with col3:
            location_filter = st.text_input("Location", "New York, NY")
        with col4:
            view_type = st.radio("View", ["List", "Calendar"], horizontal=True)
        
        # Featured event with a banner
        st.markdown("""
        <div style="position: relative; margin-bottom: 20px; border-radius: var(--radius-xl); overflow: hidden; height: 300px;">
            <img src="https://images.unsplash.com/photo-1540575467063-178a50c2df87?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" style="width: 100%; height: 100%; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0)); padding: 40px 30px 30px;">
                <div style="color: white; font-size: 0.9rem; margin-bottom: 5px;">FEATURED EVENT</div>
                <h2 style="color: white; margin-bottom: 10px; font-size: 2rem;">NYC Summer Photography Festival</h2>
                <div style="color: rgba(255,255,255,0.9); display: flex; gap: 20px; margin-bottom: 15px;">
                    <div>📅 June 24-26, 2023</div>
                    <div>📍 Central Park, New York</div>
                    <div>👥 243 attending</div>
                </div>
                <button style="background: var(--primary); color: white; border: none; padding: 8px 20px; border-radius: var(--radius-lg); font-weight: 500; cursor: pointer;">View Details</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if view_type == "Calendar":
            # Calendar view
            st.markdown("""
            <div style="background: white; border-radius: var(--radius-xl); padding: 20px; box-shadow: var(--shadow-md);">
                <div style="text-align: center; font-weight: 600; font-size: 1.2rem; margin-bottom: 15px;">June 2023</div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: 600; margin-bottom: 10px;">
                    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); grid-gap: 5px;">
                    <div style="padding: 10px; text-align: center; color: var(--neutral-400);">28</div>
                    <div style="padding: 10px; text-align: center; color: var(--neutral-400);">29</div>
                    <div style="padding: 10px; text-align: center; color: var(--neutral-400);">30</div>
                    <div style="padding: 10px; text-align: center; color: var(--neutral-400);">31</div>
                    <div style="padding: 10px; text-align: center;">1</div>
                    <div style="padding: 10px; text-align: center;">2</div>
                    <div style="padding: 10px; text-align: center;">3</div>
                    
                    <div style="padding: 10px; text-align: center;">4</div>
                    <div style="padding: 10px; text-align: center;">5</div>
                    <div style="padding: 10px; text-align: center;">6</div>
                    <div style="padding: 10px; text-align: center;">7</div>
                    <div style="padding: 10px; text-align: center;">8</div>
                    <div style="padding: 10px; text-align: center;">9</div>
                    <div style="padding: 10px; text-align: center;">10</div>
                    
                    <div style="padding: 10px; text-align: center;">11</div>
                    <div style="padding: 10px; text-align: center;">12</div>
                    <div style="padding: 10px; text-align: center;">13</div>
                    <div style="padding: 10px; text-align: center;">14</div>
                    <div style="padding: 10px; text-align: center; background: rgba(58, 134, 255, 0.1); border-radius: 50%; border: 2px solid var(--primary); color: var(--primary); font-weight: bold;">15</div>
                    <div style="padding: 10px; text-align: center; position: relative;">
                        16
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: var(--primary); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 10px; text-align: center;">17</div>
                    
                    <div style="padding: 10px; text-align: center;">18</div>
                    <div style="padding: 10px; text-align: center;">19</div>
                    <div style="padding: 10px; text-align: center; position: relative;">
                        20
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: var(--accent); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 10px; text-align: center;">21</div>
                    <div style="padding: 10px; text-align: center;">22</div>
                    <div style="padding: 10px; text-align: center;">23</div>
                    <div style="padding: 10px; text-align: center; position: relative;">
                        24
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: var(--secondary); border-radius: 50%;"></div>
                    </div>
                    
                    <div style="padding: 10px; text-align: center; position: relative;">
                        25
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: var(--secondary); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 10px; text-align: center; position: relative;">
                        26
                        <div style="position: absolute; top: 2px; right: 2px; width: 8px; height: 8px; background: var(--secondary); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 10px; text-align: center;">27</div>
                    <div style="padding: 10px; text-align: center;">28</div>
                    <div style="padding: 10px; text-align: center;">29</div>
                    <div style="padding: 10px; text-align: center;">30</div>
                    <div style="padding: 10px; text-align: center; color: var(--neutral-400);">1</div>
                </div>
                <div style="margin-top: 15px;">
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 10px; height: 10px; background: var(--primary); border-radius: 50%; margin-right: 5px;"></div>
                        <div>Your events</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 10px; height: 10px; background: var(--accent); border-radius: 50%; margin-right: 5px;"></div>
                        <div>Circle events</div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 10px; height: 10px; background: var(--secondary); border-radius: 50%; margin-right: 5px;"></div>
                        <div>Featured events</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Calendar day details
            st.markdown("### Events on June 15")
            
            # Use the event card component for events on this day
            event = {
                "name": "Sunset Photography", 
                "date": "Jun 15", 
                "time": "6:00 PM", 
                "location": "Brooklyn Bridge", 
                "circle": "NYC Photographers",
                "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."
            }
            
            st.markdown(render_event_card(event), unsafe_allow_html=True)
            
        else:
            # List view
            st.markdown("### Upcoming Events")
            
            col1, col2 = st.columns(2)
            
            # Sample events
            events = [
                {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
                {"name": "International Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown City Park", "circle": "Food Lovers", "description": "Explore various cuisines and dishes at the annual food festival."},
                {"name": "Tech Innovation Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Tech Innovation Center", "circle": "Tech Enthusiasts", "description": "Network with tech professionals and learn about the latest innovations."},
                {"name": "Morning Yoga in the Park", "date": "Jun 18", "time": "8:00 AM", "location": "Central Park", "circle": "Fitness Community", "description": "Start your day with energizing yoga in the park."}
            ]
            
            with col1:
                st.markdown(render_event_card(events[0]), unsafe_allow_html=True)
                st.markdown(render_event_card(events[2]), unsafe_allow_html=True)
            
            with col2:
                st.markdown(render_event_card(events[1]), unsafe_allow_html=True)
                st.markdown(render_event_card(events[3]), unsafe_allow_html=True)
            
            if st.button("View More Events", use_container_width=True):
                st.info("Loading more events...")
    
    with tab2:
        st.markdown("### Your Events")
        
        # Event categories
        options = st.radio("View", ["Attending", "Organized", "Past Events"], horizontal=True)
        
        if options == "Attending":
            # Sample user events
            user_events = [
                {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "status": "Confirmed", "role": "Attendee", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
                {"name": "Tech Book Club", "date": "Jun 22", "time": "7:00 PM", "status": "Pending", "role": "Attendee", "description": "Discussion of 'The Innovators' by Walter Isaacson."}
            ]
            
            if not user_events:
                st.info("You're not attending any upcoming events yet. Explore events to join!")
            else:
                for event in user_events:
                    st.markdown(f"""
                    <div class="card" style="margin-bottom: 20px; {'' if event['status'] == 'Confirmed' else 'border-left: 3px solid var(--warning);'}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h3 style="margin: 0;">{event['name']}</h3>
                            <div style="background: {'var(--primary)' if event['status'] == 'Confirmed' else 'var(--warning)'}; color: white; padding: 4px 12px; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500;">{event['status']}</div>
                        </div>
                        <div style="margin-bottom: 15px;">
                            <div style="display: flex; flex-wrap: wrap; gap: 15px; color: var(--neutral-700);">
                                <div>📅 {event['date']} at {event['time']}</div>
                                <div>👤 {event['role']}</div>
                            </div>
                        </div>
                        <p>{event['description']}</p>
                        <div style="display: flex; gap: 10px; margin-top: 15px;">
                            <button class="stButton button">View Details</button>
                            {'<button class="stButton btn-secondary">Cancel RSVP</button>' if event['status'] == 'Confirmed' else '<button class="stButton button">Confirm</button>'}
                            <button class="stButton btn-secondary">Add to Calendar</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif options == "Organized":
            # Sample organized events
            organized_events = [
                {"name": "Photography Tips & Tricks", "date": "Jul 5", "time": "7:00 PM", "attendees": 12, "capacity": 25, "description": "Learn essential photography techniques for capturing stunning images."}
            ]
            
            if not organized_events:
                st.info("You haven't organized any events yet.")
                if st.button("Create Your First Event", use_container_width=True):
                    st.session_state["events_tab"] = "create"
                    st.experimental_rerun()
            else:
                for event in organized_events:
                    attendance_percentage = int(event['attendees']/event['capacity']*100)
                    
                    st.markdown(f"""
                    <div class="card" style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h3 style="margin: 0;">{event['name']}</h3>
                            <div style="font-size: 0.9rem; color: var(--neutral-600);">Organized by you</div>
                        </div>
                        <div style="margin-bottom: 15px;">
                            <div style="display: flex; flex-wrap: wrap; gap: 15px; color: var(--neutral-700);">
                                <div>📅 {event['date']} at {event['time']}</div>
                            </div>
                        </div>
                        <p>{event['description']}</p>
                        <div style="margin: 15px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <div>Attendance</div>
                                <div>{event['attendees']}/{event['capacity']}</div>
                            </div>
                            <div style="background: var(--neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: {attendance_percentage}%;"></div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px;">
                            <button class="stButton button">Manage Attendees</button>
                            <button class="stButton btn-secondary">Edit Event</button>
                            <button class="stButton btn-danger">Cancel Event</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:  # Past Events
            # Sample past events
            past_events = [
                {"name": "City Photo Walk", "date": "May 20", "role": "Attendee", "description": "A guided photography walk through the city streets."},
                {"name": "Cooking Class", "date": "May 5", "role": "Organizer", "description": "Learned to prepare authentic Italian pasta dishes."}
            ]
            
            if not past_events:
                st.info("You don't have any past events.")
            else:
                for event in past_events:
                    st.markdown(f"""
                    <div class="card" style="margin-bottom: 20px; opacity: 0.8;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h3 style="margin: 0;">{event['name']}</h3>
                            <div style="font-size: 0.9rem; color: var(--neutral-600);">{event['role']}</div>
                        </div>
                        <div style="margin-bottom: 15px;">
                            <div style="display: flex; flex-wrap: wrap; gap: 15px; color: var(--neutral-700);">
                                <div>📅 {event['date']}</div>
                            </div>
                        </div>
                        <p>{event['description']}</p>
                        <div style="display: flex; gap: 10px; margin-top: 15px;">
                            <button class="stButton btn-secondary">View Details</button>
                            <button class="stButton btn-secondary">Photos & Media</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Create New Event")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("create_event"):
                # Basic information
                st.markdown("#### Event Details")
                name = st.text_input("Event Name", placeholder="Give your event a clear, descriptive name")
                description = st.text_area("Description", placeholder="What's your event about? Include all important details.", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("Date")
                with col2:
                    time = st.time_input("Time")
                
                location = st.text_input("Location", placeholder="Where will this event take place?")
                
                # Additional details
                st.markdown("#### Additional Information")
                col1, col2 = st.columns(2)
                with col1:
                    circle = st.selectbox("Associated Circle", ["", "NYC Photographers", "Food Lovers", "Tech Enthusiasts"])
                with col2:
                    capacity = st.number_input("Capacity (0 for unlimited)", min_value=0, value=20)
                
                col1, col2 = st.columns(2)
                with col1:
                    event_type = st.radio("Event Type", ["In-person", "Online", "Hybrid"])
                with col2:
                    visibility = st.radio("Visibility", ["Public", "Circle Members Only", "Invite Only"])
                
                # Tags
                tags = st.multiselect("Tags (helps people find your event)", 
                                    ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography"])
                
                # Cover image
                cover_image = st.file_uploader("Upload a cover image (optional)", type=["jpg", "jpeg", "png"])
                
                # Submit
                col1, col2 = st.columns(2)
                with col1:
                    submit_btn = st.form_submit_button("Create Event", use_container_width=True)
                with col2:
                    cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
                
                if submit_btn:
                    if not name:
                        st.error("Please provide a name for your event")
                    else:
                        event_id = generate_id("evt")
                        events = load_db("events")
                        events[event_id] = {
                            "event_id": event_id,
                            "name": name,
                            "description": description,
                            "date": date.isoformat(),
                            "time": str(time),
                            "location": {"name": location},
                            "organizer": st.session_state["user"]["user_id"],
                            "circle_id": circle if circle else None,
                            "capacity": capacity,
                            "event_type": event_type.lower(),
                            "visibility": visibility.lower(),
                            "tags": tags,
                            "attendees": [st.session_state["user"]["user_id"]],
                            "created_at": datetime.now().isoformat()
                        }
                        save_db("events", events)
                        
                        # Save cover image if provided
                        if cover_image:
                            image_path = f"media_gallery/event_{event_id}_cover.jpg"
                            Image.open(cover_image).save(image_path)
                            events[event_id]["cover_image"] = image_path
                            save_db("events", events)
                        
                        st.success(f"Event '{name}' created successfully!")
                        
                        # Notify circle members if associated with a circle
                        if circle:
                            add_notification(st.session_state["user"]["user_id"], "event", 
                                           f"New event in {circle}: {name}")
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3 class="card-title">Event Tips</h3>
                <div class="card-content">
                    <p><strong>Create a successful event:</strong></p>
                    <ul>
                        <li>Choose a clear, descriptive name</li>
                        <li>Provide complete details about location, time, and what to expect</li>
                        <li>Upload an eye-catching cover image</li>
                        <li>Add relevant tags to help people find your event</li>
                    </ul>
                    <p><strong>As an organizer, you can:</strong></p>
                    <ul>
                        <li>Manage the attendee list</li>
                        <li>Send updates to all registered attendees</li>
                        <li>Track attendance and engagement</li>
                        <li>Create a photo gallery after the event</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

def business_page():
    if st.session_state["user"].get("account_type") != "business":
        st.warning("This page is only available for business accounts. Please sign up for a business account to access these features.")
        if st.button("Create a Business Account"):
            st.session_state["logged_in"] = False
            st.session_state["auth_page"] = "signup"
            st.experimental_rerun()
        return
    
    st.markdown("## 💼 Business Dashboard")
    
    # Business overview header
    business_info = st.session_state.get("business", {})
    business_name = business_info.get("business_name", "Your Business")
    business_category = business_info.get("category", "")
    
    st.markdown(f"""
    <div class="card" style="background: var(--gradient-blue); color: white; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="color: white; margin-bottom: 5px;">{business_name}</h2>
                <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 15px;">{business_category}</p>
                <div style="display: flex; gap: 15px;">
                    <div style="text-align: center;">
                        <div style="font-size: 1.8rem; font-weight: 700;">245</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Followers</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.8rem; font-weight: 700;">56</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Mentions</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.8rem; font-weight: 700;">3</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Promos</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.8rem; font-weight: 700;">82%</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Rating</div>
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                {render_badge("Premium", "primary") if business_info.get("verified", False) else render_badge("Unverified", "neutral")}
                <div style="margin-top: 15px;">
                    <button class="stButton button" style="background: rgba(255, 255, 255, 0.2) !important;">Edit Profile</button>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Promotions", "Analytics", "Settings"])
    
    with tab1:
        # Quick actions row
        st.markdown("### Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Create Promotion", use_container_width=True)
        with col2:
            st.button("Post Update", use_container_width=True)
        with col3:
            st.button("Create Event", use_container_width=True)
        with col4:
            st.button("Contact Followers", use_container_width=True)
        
        # Activity and engagement
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### Recent Activity")
            
            activities = [
                {"user": "JaneDoe", "action": "mentioned your business in a post", "time": "2h ago", "icon": "📸"},
                {"user": "PhotoLover", "action": "used your promotion code", "time": "5h ago", "icon": "🎁"},
                {"user": "MikeT", "action": "tagged your business in a photo", "time": "1d ago", "icon": "📸"},
                {"user": "FoodieClub", "action": "added your business to their recommended list", "time": "2d ago", "icon": "👍"}
            ]
            
            for activity in activities:
                st.markdown(render_activity_item(
                    activity['user'], 
                    activity['action'], 
                    activity['time'],
                    activity['icon']
                ), unsafe_allow_html=True)
            
            if st.button("View All Activity", use_container_width=True):
                st.info("Loading activity history...")
        
        with col2:
            st.markdown("### Engagement Summary")
            
            # Engagement metrics
            st.markdown("""
            <div class="card">
                <h3 class="card-title">Last 7 Days</h3>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>Profile Views</div>
                        <div style="font-weight: 600;">127</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 75%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>Media Tags</div>
                        <div style="font-weight: 600;">23</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 40%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>New Followers</div>
                        <div style="font-weight: 600;">18</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 30%;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div>Promotion Claims</div>
                        <div style="font-weight: 600;">12</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 25%;"></div>
        </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Business Circle
        st.markdown("### Your Business Circle")
        if not business_info.get("has_circle", False):
            st.markdown("""
            <div class="card">
                <h3 class="card-title">Create Your Business Circle</h3>
                <p>Connect directly with your customers by creating a dedicated circle for your business. Share updates, promotions, and events with your community.</p>
                <button class="stButton button">Create Business Circle</button>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("Your business circle has 86 members")
            st.button("Manage Circle", use_container_width=True)
        
        # Media mentions
        st.markdown("### Media Mentions")
        st.markdown("Recent photos and posts that mention your business")
        
        # Grid of media
        st.markdown("""
        <div class="gallery-container">
            <div class="gallery-item">
                <img src="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cmVzdGF1cmFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" class="gallery-image">
                <div class="gallery-overlay">
                    <div class="gallery-title">@user1</div>
                    <div class="gallery-meta">
                        <div>2h ago</div>
                        <div>❤️ 24</div>
                    </div>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://images.unsplash.com/photo-1578474846511-04ba529f0b88?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Y2FmZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" class="gallery-image">
                <div class="gallery-overlay">
                    <div class="gallery-title">@user2</div>
                    <div class="gallery-meta">
                        <div>5h ago</div>
                        <div>❤️ 18</div>
                    </div>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://images.unsplash.com/photo-1481833761820-0509d3217039?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8cmVzdGF1cmFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" class="gallery-image">
                <div class="gallery-overlay">
                    <div class="gallery-title">@user3</div>
                    <div class="gallery-meta">
                        <div>1d ago</div>
                        <div>❤️ 42</div>
                    </div>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Y2FmZSUyMGZvb2R8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60" class="gallery-image">
                <div class="gallery-overlay">
                    <div class="gallery-title">@user4</div>
                    <div class="gallery-meta">
                        <div>2d ago</div>
                        <div>❤️ 15</div>
                    </div>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://images.unsplash.com/photo-1525610553991-2bede1a236e2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Nnx8Y2FmZSUyMGZvb2R8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60" class="gallery-image">
                <div class="gallery-overlay">
                    <div class="gallery-title">@user5</div>
                    <div class="gallery-meta">
                        <div>3d ago</div>
                        <div>❤️ 29</div>
                    </div>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://images.unsplash.com/photo-1515215316771-2742baa337f4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8Y2FmZSUyMGZvb2R8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60" class="gallery-image">
                <div class="gallery-overlay">
                    <div class="gallery-title">@user6</div>
                    <div class="gallery-meta">
                        <div>5d ago</div>
                        <div>❤️ 33</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View All Mentions", use_container_width=True):
            st.info("Loading all mentions...")
    
    with tab2:
        st.markdown("### Manage Promotions")
        st.markdown("Create and track special offers for your followers")
        
        # Existing promotions
        st.markdown("#### Active Promotions")
        
        # Sample promotions
        promotions = [
            {"name": "Summer Special", "offer": "20% off all items", "description": "Enjoy summer savings on all menu items. Limited time only!", "requirements": "Show this offer to the cashier when ordering.", "start_date": "2023-06-01", "end_date": "2023-08-31", "claimed_by": ["usr_1", "usr_2", "usr_3"]},
            {"name": "Photo Contest", "offer": "Win a free camera", "description": "Submit your best photos for a chance to win a professional camera.", "requirements": "Post 3 photos with #PhotoContest and tag our business.", "start_date": "2023-06-15", "end_date": "2023-07-15", "claimed_by": ["usr_1"]}
        ]
        
        if promotions:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(render_promotion_card(promotions[0], interactive=False), unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Edit", key="edit_promo_1", use_container_width=True)
                with col2:
                    st.button("End Promotion", key="end_promo_1", use_container_width=True)
            
            with col2:
                st.markdown(render_promotion_card(promotions[1], interactive=False), unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Edit", key="edit_promo_2", use_container_width=True)
                with col2:
                    st.button("End Promotion", key="end_promo_2", use_container_width=True)
        else:
            st.info("You don't have any active promotions")
        
        # Create promotion form
        st.markdown("#### Create New Promotion")
        with st.form("create_promotion"):
            col1, col2 = st.columns(2)
            with col1:
                promo_name = st.text_input("Promotion Name", placeholder="Summer Special, New Customer Discount, etc.")
            with col2:
                offer_type = st.selectbox("Offer Type", ["Percentage Discount", "Fixed Amount Off", "Free Item", "Buy One Get One", "Custom"])
            
            if offer_type == "Percentage Discount":
                col1, col2 = st.columns(2)
                with col1:
                    discount_percent = st.number_input("Discount Percentage", min_value=1, max_value=100, value=20)
                with col2:
                    min_purchase = st.number_input("Minimum Purchase ($)", min_value=0.0, value=0.0, step=5.0)
                
                offer_text = f"{discount_percent}% off"
                if min_purchase > 0:
                    offer_text += f" on purchases over ${min_purchase:.2f}"
            else:
                offer_text = st.text_input("Offer Details", placeholder="Describe your offer...")
            
            requirements = st.text_input("Requirements", placeholder="Post with #YourBusiness, Tag in a photo, etc.")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                end_date = st.date_input("End Date")
            
            tags = st.multiselect("Relevant Tags", ["Food", "Drink", "Retail", "Sale", "Summer", "Holiday", "Special"])
            
            col1, col2 = st.columns(2)
            with col1:
                submit_btn = st.form_submit_button("Launch Promotion", use_container_width=True)
            with col2:
                cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit_btn:
                if not promo_name or not offer_text:
                    st.error("Please fill in all required fields")
                else:
                    promo_id = generate_id("promo")
                    promotions_db = load_db("promotions")
                    promotions_db[promo_id] = {
                        "promo_id": promo_id,
                        "name": promo_name,
                        "business_id": st.session_state["user"]["user_id"],
                        "offer": offer_text,
                        "description": f"Limited time offer from {business_name}",
                        "requirements": requirements,
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "tags": tags,
                        "claimed_by": [],
                        "created_at": datetime.now().isoformat()
                    }
                    save_db("promotions", promotions_db)
                    st.success("Promotion launched successfully!")
    
    with tab3:
        st.markdown("### Business Analytics")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days", "This year", "Custom range"])
        with col2:
            if date_range == "Custom range":
                start_date = st.date_input("From")
                end_date = st.date_input("To")
        
        # Key metrics
        st.markdown("#### Key Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_stat_card("1,247", "Profile Views", "👁️", change=12), unsafe_allow_html=True)
        with col2:
            st.markdown(render_stat_card("287", "Media Tags", "📸", change=8), unsafe_allow_html=True)
        with col3:
            st.markdown(render_stat_card("56", "Promotion Claims", "🎁", change=-3), unsafe_allow_html=True)
        with col4:
            st.markdown(render_stat_card("32", "New Followers", "👥", change=15), unsafe_allow_html=True)
        
        # Visual charts
        st.markdown("#### Engagement Over Time")
        
        st.markdown("""
        <div class="card">
            <div style="height: 250px; position: relative;">
                <!-- Simulated chart - in a real app, this would be an actual chart -->
                <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 200px; display: flex; align-items: flex-end;">
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 30%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 45%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 60%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 40%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 70%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 85%;"></div>
                    <div style="flex: 1; margin: 0 2px; background: var(--primary); height: 65%;"></div>
                </div>
                <div style="position: absolute; bottom: -25px; left: 0; right: 0; display: flex; justify-content: space-between; padding: 0 10px;">
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Mon</div>
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Tue</div>
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Wed</div>
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Thu</div>
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Fri</div>
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Sat</div>
                    <div style="font-size: 0.8rem; color: var(--neutral-600);">Sun</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Demographic data
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### User Demographics")
            st.markdown("""
            <div class="card">
                <div style="margin-bottom: 15px;">
                    <div style="font-weight: 500; margin-bottom: 5px;">Age Groups</div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">18-24</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 25%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">25%</div>
                    </div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">25-34</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 40%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">40%</div>
                    </div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">35-44</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 20%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">20%</div>
                    </div>
                    <div style="display: flex;">
                        <div style="width: 80px;">45+</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 15%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">15%</div>
                    </div>
                </div>
                
                <div>
                    <div style="font-weight: 500; margin-bottom: 5px;">Gender</div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">Female</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 58%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">58%</div>
                    </div>
                    <div style="display: flex; margin-bottom: 5px;">
                        <div style="width: 80px;">Male</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 39%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">39%</div>
                    </div>
                    <div style="display: flex;">
                        <div style="width: 80px;">Other</div>
                        <div style="flex-grow: 1;">
                            <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                                <div style="background: var(--primary); height: 100%; width: 3%;"></div>
                            </div>
                        </div>
                        <div style="width: 40px; text-align: right;">3%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Top Locations")
            st.markdown("""
            <div class="card">
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">New York, NY</div>
                        <div>45%</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 45%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">Brooklyn, NY</div>
                        <div>25%</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 25%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">Queens, NY</div>
                        <div>15%</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 15%;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div style="font-weight: 500;">Other</div>
                        <div>15%</div>
                    </div>
                    <div style="background: var(--neutral-200); height: 15px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--primary); height: 100%; width: 15%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export options
        st.markdown("#### Data Export")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Export as CSV", use_container_width=True)
        with col2:
            st.button("Export as PDF", use_container_width=True)
        with col3:
            st.button("Schedule Reports", use_container_width=True)
    
    with tab4:
        st.markdown("### Business Settings")
        
        # Profile settings
        st.markdown("#### Business Profile")
        with st.form("business_profile"):
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("Business Name", value=business_info.get("business_name", ""))
            with col2:
                category = st.selectbox("Business Category", 
                                      ["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"],
                                      index=["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"].index(business_info.get("category", "Other")))
            
            description = st.text_area("Business Description", value=business_info.get("description", ""), height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_input("Primary Address", value=business_info.get("locations", [{}])[0].get("address", ""))
            with col2:
                website = st.text_input("Website", value=business_info.get("website", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Business Phone", value=business_info.get("phone", ""))
            with col2:
                email = st.text_input("Business Email", value=business_info.get("email", ""))
            
            business_hours = st.text_area("Business Hours", value=business_info.get("hours", ""), height=100, 
                                        placeholder="Monday: 9am-5pm\nTuesday: 9am-5pm\netc.")
            
            # Logo and cover image
            st.markdown("#### Business Images")
            col1, col2 = st.columns(2)
            with col1:
                logo = st.file_uploader("Business Logo", type=["png", "jpg", "jpeg"])
            with col2:
                cover = st.file_uploader("Cover Image", type=["png", "jpg", "jpeg"])
            
            st.markdown("#### Social Media Links")
            col1, col2 = st.columns(2)
            with col1:
                instagram = st.text_input("Instagram", value=business_info.get("social", {}).get("instagram", ""))
            with col2:
                facebook = st.text_input("Facebook", value=business_info.get("social", {}).get("facebook", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                twitter = st.text_input("Twitter", value=business_info.get("social", {}).get("twitter", ""))
            with col2:
                linkedin = st.text_input("LinkedIn", value=business_info.get("social", {}).get("linkedin", ""))
            
            # Submit buttons
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Save Changes", use_container_width=True)
            with col2:
                cancel_button = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit_button:
                # Update business info
                businesses = load_db("businesses")
                business_id = business_info.get("business_id")
                
                if business_id and business_id in businesses:
                    businesses[business_id].update({
                        "business_name": business_name,
                        "category": category,
                        "description": description,
                        "locations": [{"address": address}],
                        "website": website,
                        "phone": phone,
                        "email": email,
                        "hours": business_hours,
                        "social": {
                            "instagram": instagram,
                            "facebook": facebook,
                            "twitter": twitter,
                            "linkedin": linkedin
                        }
                    })
                    
                    # Save images if provided
                    if logo:
                        logo_path = f"media_gallery/business_{business_id}_logo.jpg"
                        Image.open(logo).save(logo_path)
                        businesses[business_id]["logo"] = logo_path
                    
                    if cover:
                        cover_path = f"media_gallery/business_{business_id}_cover.jpg"
                        Image.open(cover).save(cover_path)
                        businesses[business_id]["cover_image"] = cover_path
                    
                    save_db("businesses", businesses)
                    st.session_state["business"] = businesses[business_id]
                    st.success("Business profile updated successfully!")
        
        # Verification status
        st.markdown("#### Business Verification")
        if business_info.get("verified", False):
            st.markdown("""
            <div class="card" style="background: rgba(56, 176, 0, 0.1); border-left: 3px solid var(--success);">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2rem; color: var(--success);">✓</div>
                    <div>
                        <h3 style="color: var(--success); margin-bottom: 5px;">Your business is verified!</h3>
                        <p style="margin: 0;">Enjoy all premium features and increased visibility across the platform.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <h3 class="card-title">Verify Your Business</h3>
                <p>Get verified to unlock premium features and build trust with users. Verified businesses get:</p>
                <ul>
                    <li>Higher visibility in search results</li>
                    <li>A verification badge on your profile</li>
                    <li>Access to premium analytics</li>
                    <li>Ability to run advanced promotions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("verification_form"):
                business_license = st.file_uploader("Business License or Registration")
                id_proof = st.file_uploader("ID Proof of Owner/Representative")
                proof_of_address = st.file_uploader("Proof of Business Address")
                website = st.text_input("Business Website")
                additional_info = st.text_area("Additional Information", height=100)
                
                st.form_submit_button("Submit for Verification", use_container_width=True)

def settings_page():
    st.markdown("## ⚙️ Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Account", "Notifications", "Privacy", "Support"])
    
    with tab1:
        st.markdown("### Account Settings")
        
        # Profile picture
        col1, col2 = st.columns([1, 3])
        with col1:
            # Display user avatar
            user_name = st.session_state["user"].get("full_name", "User")
            avatar_data = create_user_avatar(user_name)
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="data:image/png;base64,{avatar_data}" class="profile-pic" style="width: 100px; height: 100px; border-radius: 50%;">
                <button style="margin-top: 10px; background: transparent; border: none; color: var(--primary); font-size: 0.9rem;">Change</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.form("account_settings"):
                col1, col2 = st.columns(2)
                with col1:
                    full_name = st.text_input("Full Name", value=st.session_state["user"].get("full_name", ""))
                with col2:
                    username = st.text_input("Username", value=[k for k, v in load_db("users").items() if v["user_id"] == st.session_state["user"]["user_id"]][0] if "user_id" in st.session_state["user"] else "", disabled=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    email = st.text_input("Email", value=st.session_state["user"].get("email", ""))
                with col2:
                    location = st.text_input("Location", value=st.session_state["user"].get("location", {}).get("city", ""))
                
                interests = st.multiselect("Interests", 
                                        ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography", "Books", "Movies"],
                                        default=st.session_state["user"].get("interests", []))
                
                biography = st.text_area("Bio", height=100, value=st.session_state["user"].get("bio", ""), 
                                      placeholder="Tell others about yourself...")
                
                col1, col2 = st.columns(2)
                with col1:
                    update_btn = st.form_submit_button("Update Profile", use_container_width=True)
                with col2:
                    cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
                
                if update_btn:
                    users = load_db("users")
                    username_key = [k for k, v in users.items() if v["user_id"] == st.session_state["user"]["user_id"]][0]
                    
                    users[username_key].update({
                        "full_name": full_name,
                        "email": email,
                        "location": {"city": location},
                        "interests": interests,
                        "bio": biography
                    })
                    
                    save_db("users", users)
                    st.session_state["user"] = users[username_key]
                    st.success("Profile updated successfully!")
        
        # Password and security
        st.markdown("### Password & Security")
        with st.form("security_form"):
            current_password = st.text_input("Current Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                new_password = st.text_input("New Password", type="password")
            with col2:
                confirm_password = st.text_input("Confirm New Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit_btn = st.form_submit_button("Update Password", use_container_width=True)
            
            if submit_btn:
                if not current_password:
                    st.error("Please enter your current password")
                elif not new_password or not confirm_password:
                    st.error("Please enter and confirm your new password")
                elif new_password != confirm_password:
                    st.error("New passwords don't match")
                else:
                    # Verify current password and update
                    users = load_db("users")
                    username_key = [k for k, v in users.items() if v["user_id"] == st.session_state["user"]["user_id"]][0]
                    
                    if verify_password(current_password, users[username_key]["password"]):
                        users[username_key]["password"] = hash_password(new_password)
                        save_db("users", users)
                        st.success("Password updated successfully!")
                    else:
                        st.error("Current password is incorrect")
        
        # Account management
        st.markdown("### Account Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download My Data", use_container_width=True):
                st.info("Your data is being prepared for download. This may take a few minutes.")
        with col2:
            if st.button("Delete Account", use_container_width=True):
                st.warning("⚠️ This action cannot be undone. All your data will be permanently deleted.")
                confirm_delete = st.checkbox("I understand the consequences")
                if confirm_delete:
                    if st.button("Confirm Delete"):
                        st.error("Account marked for deletion. You will be logged out in 5 seconds.")
                        # In a real app, would handle account deletion process
    
    with tab2:
        st.markdown("### Notification Settings")
        
        # Email notifications
        st.markdown("#### Email Notifications")
        col1, col2 = st.columns(2)
        with col1:
            email_circle = st.checkbox("Circle updates", value=True)
            email_events = st.checkbox("Event reminders", value=True)
            email_followers = st.checkbox("New followers", value=True)
        with col2:
            email_promos = st.checkbox("Promotions and offers", value=True)
            email_mentions = st.checkbox("Media mentions", value=True)
            email_newsletter = st.checkbox("Newsletter", value=False)
        
        # Push notifications
        st.markdown("#### Push Notifications")
        col1, col2 = st.columns(2)
        with col1:
            push_circle = st.checkbox("Circle activity", value=True)
            push_events = st.checkbox("Event notifications", value=True)
            push_followers = st.checkbox("New followers", value=True)
        with col2:
            push_promos = st.checkbox("Promotion alerts", value=True)
            push_mentions = st.checkbox("Media mentions", value=True)
            push_messages = st.checkbox("Direct messages", value=True)
        
        # Notification schedule
        st.markdown("#### Notification Schedule")
        quiet_hours = st.checkbox("Enable quiet hours")
        if quiet_hours:
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.time_input("Start time", value=datetime.strptime("22:00", "%H:%M").time())
            with col2:
                end_time = st.time_input("End time", value=datetime.strptime("07:00", "%H:%M").time())
        
        if st.button("Save Notification Preferences", use_container_width=True):
            # In a real app, would save these preferences to the user's profile
            st.success("Notification preferences saved!")
    
    with tab3:
        st.markdown("### Privacy Settings")
        
        # Profile privacy
        st.markdown("#### Profile Visibility")
        profile_visibility = st.radio("Who can see my profile", ["Everyone", "Circle Members Only", "Followers Only"])
        
        # Content privacy
        st.markdown("#### Content Privacy")
        col1, col2 = st.columns(2)
        with col1:
            location_share = st.checkbox("Share my location with posts", value=True)
            media_visibility = st.radio("Media visibility", ["Public", "Circle Members", "Followers Only"])
        with col2:
            circle_visibility = st.radio("My circles visibility", ["Public", "Followers Only", "Private"])
            event_visibility = st.radio("Event attendance visibility", ["Public", "Circle Members", "Private"])
        
        # Data sharing
        st.markdown("#### Data Usage")
        col1, col2 = st.columns(2)
        with col1:
            personalization = st.checkbox("Personalize my experience based on activity", value=True)
            recommendations = st.checkbox("Show personalized recommendations", value=True)
        with col2:
            third_party = st.checkbox("Allow third-party services", value=False)
            analytics = st.checkbox("Contribute to anonymous analytics", value=True)
        
        if st.button("Save Privacy Settings", use_container_width=True):
            # In a real app, would save these preferences to the user's profile
            st.success("Privacy settings updated!")
    
    with tab4:
        st.markdown("### Help & Support")
        
        # Report issues
        st.markdown("#### Report a Problem")
        with st.form("report_issue"):
            issue_type = st.selectbox("Issue Type", 
                                    ["Bug Report", "Feature Request", "Account Issue", "Content Moderation", "Other"])
            
            issue_description = st.text_area("Describe the issue", height=150, 
                                         placeholder="Please provide details about the issue you're experiencing...")
            
            severity = st.slider("How severely does this affect your experience?", 1, 5, 3)
            
            include_logs = st.checkbox("Include app logs to help troubleshooting", value=True)
            
            file_upload = st.file_uploader("Attach screenshots or relevant files", type=["jpg", "jpeg", "png", "pdf"])
            
            submit_btn = st.form_submit_button("Submit Report", use_container_width=True)
            
            if submit_btn:
                if not issue_description:
                    st.error("Please describe the issue")
                else:
                    st.success("Your report has been submitted. Our team will review it as soon as possible.")
        
        # Report content
        st.markdown("#### Report Content")
        with st.form("report_content"):
            content_type = st.selectbox("Content Type", ["Media", "Circle", "Event", "User Profile", "Comment"])
            content_id = st.text_input("Content URL or ID", placeholder="Paste the URL or ID of the content")
            reason = st.selectbox("Reason", 
                               ["Inappropriate content", "Spam", "Misinformation", "Harassment", "Hate speech", "Other"])
            details = st.text_area("Additional Details", height=100, 
                                 placeholder="Please provide more information about the issue...")
            
            submit_btn = st.form_submit_button("Submit Report", use_container_width=True)
            
            if submit_btn:
                if not content_id:
                    st.error("Please provide the URL or ID of the content")
                else:
                    report_id = generate_id("rep")
                    reports = load_db("reports")
                    reports.append({
                        "report_id": report_id,
                        "reporter_id": st.session_state["user"]["user_id"],
                        "content_type": content_type.lower(),
                        "content_id": content_id,
                        "reason": reason,
                        "details": details,
                        "status": "pending",
                        "timestamp": datetime.now().isoformat()
                    })
                    save_db("reports", reports)
                    st.success("Report submitted. Our team will review it shortly.")
        
        # FAQ and help resources
        st.markdown("#### Frequently Asked Questions")
        with st.expander("How do I create a Circle?"):
            st.write("""
            To create a Circle:
            1. Navigate to the Circles page
            2. Click on the "Create Circle" tab
            3. Fill in the Circle details including name, description, and settings
            4. Click "Create Circle" to finalize
            
            Your new Circle will be created immediately, and you can start inviting members.
            """)
        
        with st.expander("How do promotions work?"):
            st.write("""
            Promotions allow businesses to offer special deals to Atmosphere users:
            1. Businesses create promotional offers with specific requirements
            2. Users complete the requirements (like posting photos with specific tags)
            3. Users receive the promotion in their notification feed
            4. Users can claim the promotion at the business location
            
            Requirements vary by promotion, so check the details of each offer.
            """)
        
        with st.expander("How can I change my privacy settings?"):
            st.write("""
            You can manage your privacy settings at any time:
            1. Go to Settings > Privacy
            2. Adjust your profile visibility, content privacy, and data sharing preferences
            3. Save your changes
            
            Changes to privacy settings take effect immediately.
            """)
        
        # Contact support
        st.markdown("#### Contact Support")
        st.info("Our support team is available 24/7 to help you with any issues or questions.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Email Support", use_container_width=True)
        with col2:
            st.button("Live Chat", use_container_width=True)

# ===== NOTIFICATION BELL =====
def notification_bell():
    notifications = load_db("notifications").get(st.session_state["user"]["user_id"], [])
    unread = sum(1 for n in notifications if not n.get("read", False))
    
    with st.sidebar:
        # Notification bell with badge
        if unread > 0:
            notification_button = st.button(f"🔔 Notifications ({unread})", use_container_width=True)
        else:
            notification_button = st.button("🔔 Notifications", use_container_width=True)
        
        if notification_button:
            if "show_notifications" in st.session_state and st.session_state["show_notifications"]:
                st.session_state["show_notifications"] = False
            else:
                st.session_state["show_notifications"] = True
        
        # Display notifications if toggled
        if st.session_state.get("show_notifications"):
            st.markdown("""
            <div class="card" style="margin-top: 10px;">
                <h3 class="card-title" style="margin-bottom: 15px;">Recent Notifications</h3>
            """, unsafe_allow_html=True)
            
            if not notifications:
                st.markdown("""
                <div style="padding: 10px; text-align: center; color: var(--neutral-600);">
                    You don't have any notifications yet
                </div>
                """, unsafe_allow_html=True)
            else:
                # Sort notifications by timestamp, newest first
                sorted_notifications = sorted(notifications, key=lambda x: x.get("timestamp", ""), reverse=True)
                
                # Display 5 most recent notifications
                for note in sorted_notifications[:5]:
                    st.markdown(render_notification_item(note), unsafe_allow_html=True)
            
            # Mark all as read and view all buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark all read", use_container_width=True):
                    # Mark all notifications as read
                    notifications_db = load_db("notifications")
                    if st.session_state["user"]["user_id"] in notifications_db:
                        for note in notifications_db[st.session_state["user"]["user_id"]]:
                            note["read"] = True
                        save_db("notifications", notifications_db)
                        st.experimental_rerun()
            with col2:
                if st.button("View all", use_container_width=True):
                    # View all notifications
                    st.session_state["page"] = "notifications"
                    st.experimental_rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ===== MAIN APP FLOW =====
def main():
    # Initialize session state variables if they don't exist
    if "show_notifications" not in st.session_state:
        st.session_state["show_notifications"] = False
    
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"
    
    # Sidebar navigation
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align: center; padding: 10px 0; margin-bottom: 20px;">
            <h1 style="color: white; font-size: 1.8rem; font-weight: 700; margin: 0;">🌍 Atmosphere</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if "logged_in" in st.session_state:
            # User info
            user_name = st.session_state['user']['full_name']
            avatar_data = create_user_avatar(user_name)
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <img src="data:image/png;base64,{avatar_data}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; border: 2px solid white;">
                <div>
                    <div style="font-weight: 600; color: white;">{user_name}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">@{st.session_state['user'].get('email', '').split('@')[0]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Navigation
            pages = {
                "🏠 Home": home_page,
                "🔍 Explore": explore_page,
                "📸 Media": media_page,
                "👥 Circles": circles_page,
                "📅 Events": events_page,
                "💼 Business": business_page,
                "⚙️ Settings": settings_page
            }
            
            # Check if page is stored in session state
            if "page" not in st.session_state:
                st.session_state["page"] = "🏠 Home"
            
            selected_page = st.radio("", list(pages.keys()), 
                                    index=list(pages.keys()).index(st.session_state["page"]) if st.session_state["page"] in pages else 0,
                                    label_visibility="collapsed")
            
            # Update page in session state
            st.session_state["page"] = selected_page
            
            # Notification bell
            notification_bell()
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
        else:
            # Welcome message for non-logged in users
            st.markdown("""
            <div style="color: white; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 10px;">Welcome to Atmosphere</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Connect with your community</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Login/Signup buttons
            if st.button("Login", use_container_width=True):
                st.session_state["auth_page"] = "login"
                st.experimental_rerun()
            
            if st.button("Sign Up", use_container_width=True):
                st.session_state["auth_page"] = "signup"
                st.experimental_rerun()
    
    # Main content area
    if "logged_in" in st.session_state:
        # Call the appropriate page function
        pages[selected_page]()
    else:
        if st.session_state["auth_page"] == "login":
            login()
        else:
            signup()

if __name__ == "__main__":
    main()
