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

# ===== ULTRA MODERN UI STYLING (2025 EDITION) =====
def load_css():
    st.markdown("""
    <style>
        /* ULTRA MODERN DESIGN SYSTEM - 2025 EDITION */
        
        /* Import custom fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        /* Root Design Tokens */
        :root {
            /* Color System - Futuristic Palette */
            --color-primary-50: #F0F7FF;
            --color-primary-100: #E0EFFF;
            --color-primary-200: #C0DFFF;
            --color-primary-300: #92C8FF;
            --color-primary-400: #5EAAFC;
            --color-primary-500: #3D8BFD;
            --color-primary-600: #2668E0;
            --color-primary-700: #1E54B7;
            --color-primary-800: #193F88;
            --color-primary-900: #112A59;
            
            --color-secondary-50: #F2EEFE;
            --color-secondary-100: #E4DDFC;
            --color-secondary-200: #CCBBF9;
            --color-secondary-300: #AC8FF5;
            --color-secondary-400: #9675F2;
            --color-secondary-500: #805BE0;
            --color-secondary-600: #6A46C7;
            --color-secondary-700: #5936A2;
            --color-secondary-800: #452A7B;
            --color-secondary-900: #311D59;
            
            --color-tertiary-50: #FFF0F9;
            --color-tertiary-100: #FFE0F3;
            --color-tertiary-200: #FFC1E7;
            --color-tertiary-300: #FF9FD7;
            --color-tertiary-400: #FF76C6;
            --color-tertiary-500: #FF4DB6;
            --color-tertiary-600: #E93DA5;
            --color-tertiary-700: #C2328A;
            --color-tertiary-800: #962970;
            --color-tertiary-900: #6F2053;
            
            --color-success-50: #ECFDF5;
            --color-success-100: #D1FAE5;
            --color-success-200: #A7F3D0;
            --color-success-300: #6EE7B7;
            --color-success-400: #34D399;
            --color-success-500: #10B981;
            --color-success-600: #059669;
            --color-success-700: #047857;
            --color-success-800: #065F46;
            --color-success-900: #064E3B;
            
            --color-warning-50: #FFFBEB;
            --color-warning-100: #FEF3C7;
            --color-warning-200: #FDE68A;
            --color-warning-300: #FCD34D;
            --color-warning-400: #FBBF24;
            --color-warning-500: #F59E0B;
            --color-warning-600: #D97706;
            --color-warning-700: #B45309;
            --color-warning-800: #92400E;
            --color-warning-900: #78350F;
            
            --color-error-50: #FEF2F2;
            --color-error-100: #FEE2E2;
            --color-error-200: #FECACA;
            --color-error-300: #FCA5A5;
            --color-error-400: #F87171;
            --color-error-500: #EF4444;
            --color-error-600: #DC2626;
            --color-error-700: #B91C1C;
            --color-error-800: #991B1B;
            --color-error-900: #7F1D1D;
            
            /* Neutral System */
            --color-neutral-50: #F9FAFB;
            --color-neutral-100: #F3F4F6;
            --color-neutral-200: #E5E7EB;
            --color-neutral-300: #D1D5DB;
            --color-neutral-400: #9CA3AF;
            --color-neutral-500: #6B7280;
            --color-neutral-600: #4B5563;
            --color-neutral-700: #374151;
            --color-neutral-800: #1F2937;
            --color-neutral-900: #111827;
            
            /* Glass Effect */
            --glass-white: rgba(255, 255, 255, 0.8);
            --glass-black: rgba(0, 0, 0, 0.7);
            --glass-blur: 12px;
            --glass-border: 1px solid rgba(255, 255, 255, 0.125);
            
            /* Shadows */
            --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
            --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -1px rgba(15, 23, 42, 0.04);
            --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.04);
            --shadow-xl: 0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 10px 10px -5px rgba(15, 23, 42, 0.04);
            --shadow-2xl: 0 25px 50px -12px rgba(15, 23, 42, 0.25);
            --shadow-inner: inset 0 2px 4px 0 rgba(15, 23, 42, 0.04);
            
            /* Special effects shadows */
            --shadow-blue-sm: 0 2px 8px rgba(61, 139, 253, 0.2);
            --shadow-blue-md: 0 4px 16px rgba(61, 139, 253, 0.4);
            --shadow-blue-lg: 0 8px 32px rgba(61, 139, 253, 0.6);
            
            --shadow-purple-sm: 0 2px 8px rgba(128, 91, 224, 0.2);
            --shadow-purple-md: 0 4px 16px rgba(128, 91, 224, 0.4);
            --shadow-purple-lg: 0 8px 32px rgba(128, 91, 224, 0.6);
            
            --shadow-pink-sm: 0 2px 8px rgba(255, 77, 182, 0.2);
            --shadow-pink-md: 0 4px 16px rgba(255, 77, 182, 0.4);
            --shadow-pink-lg: 0 8px 32px rgba(255, 77, 182, 0.6);
            
            /* Gradients */
            --gradient-blue: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-400) 100%);
            --gradient-purple: linear-gradient(135deg, var(--color-secondary-600) 0%, var(--color-secondary-400) 100%);
            --gradient-pink: linear-gradient(135deg, var(--color-tertiary-600) 0%, var(--color-tertiary-400) 100%);
            --gradient-blue-purple: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-secondary-600) 100%);
            --gradient-purple-pink: linear-gradient(135deg, var(--color-secondary-600) 0%, var(--color-tertiary-600) 100%);
            --gradient-blue-pink: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-tertiary-600) 100%);
            --gradient-success: linear-gradient(135deg, var(--color-success-600) 0%, var(--color-success-400) 100%);
            --gradient-warning: linear-gradient(135deg, var(--color-warning-600) 0%, var(--color-warning-400) 100%);
            --gradient-error: linear-gradient(135deg, var(--color-error-600) 0%, var(--color-error-400) 100%);
            
            /* Glassmorphism gradients */
            --glass-gradient-blue: linear-gradient(135deg, rgba(38, 104, 224, 0.8) 0%, rgba(94, 170, 252, 0.8) 100%);
            --glass-gradient-purple: linear-gradient(135deg, rgba(106, 70, 199, 0.8) 0%, rgba(150, 117, 242, 0.8) 100%);
            --glass-gradient-pink: linear-gradient(135deg, rgba(233, 61, 165, 0.8) 0%, rgba(255, 118, 198, 0.8) 100%);
            
            /* Typography */
            --font-sans: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-heading: 'Space Grotesk', sans-serif;
            --font-body: 'DM Sans', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            
            /* Spacing */
            --spacing-px: 1px;
            --spacing-0: 0px;
            --spacing-0-5: 0.125rem;
            --spacing-1: 0.25rem;
            --spacing-1-5: 0.375rem;
            --spacing-2: 0.5rem;
            --spacing-2-5: 0.625rem;
            --spacing-3: 0.75rem;
            --spacing-3-5: 0.875rem;
            --spacing-4: 1rem;
            --spacing-5: 1.25rem;
            --spacing-6: 1.5rem;
            --spacing-7: 1.75rem;
            --spacing-8: 2rem;
            --spacing-9: 2.25rem;
            --spacing-10: 2.5rem;
            --spacing-11: 2.75rem;
            --spacing-12: 3rem;
            --spacing-14: 3.5rem;
            --spacing-16: 4rem;
            --spacing-20: 5rem;
            --spacing-24: 6rem;
            --spacing-28: 7rem;
            --spacing-32: 8rem;
            --spacing-36: 9rem;
            --spacing-40: 10rem;
            --spacing-44: 11rem;
            --spacing-48: 12rem;
            --spacing-52: 13rem;
            --spacing-56: 14rem;
            --spacing-60: 15rem;
            --spacing-64: 16rem;
            --spacing-72: 18rem;
            --spacing-80: 20rem;
            --spacing-96: 24rem;
            
            /* Border Radius */
            --radius-none: 0px;
            --radius-sm: 0.125rem;
            --radius-md: 0.25rem;
            --radius-lg: 0.5rem;
            --radius-xl: 0.75rem;
            --radius-2xl: 1rem;
            --radius-3xl: 1.5rem;
            --radius-4xl: 2rem;
            --radius-full: 9999px;
            
            /* Animation */
            --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
            --ease-in: cubic-bezier(0.4, 0, 1, 1);
            --ease-out: cubic-bezier(0, 0, 0.2, 1);
            --ease-linear: linear;
            
            --duration-75: 75ms;
            --duration-100: 100ms;
            --duration-150: 150ms;
            --duration-200: 200ms;
            --duration-300: 300ms;
            --duration-500: 500ms;
            --duration-700: 700ms;
            --duration-1000: 1000ms;
        }
        
        /* BASE STYLES */
        body {
            font-family: var(--font-body);
            color: var(--color-neutral-800);
            background-color: var(--color-neutral-50);
            line-height: 1.5;
            font-size: 16px;
        }
        
        /* Typography Resets */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-heading);
            font-weight: 700;
            letter-spacing: -0.025em;
            color: var(--color-neutral-900);
            margin: 0 0 var(--spacing-4) 0;
        }
        
        h1 {
            font-size: 2.5rem;
            line-height: 1.1;
        }
        
        h2 {
            font-size: 2rem;
            line-height: 1.2;
        }
        
        h3 {
            font-size: 1.5rem;
            line-height: 1.3;
        }
        
        h4 {
            font-size: 1.25rem;
            line-height: 1.4;
        }
        
        h5 {
            font-size: 1.125rem;
            line-height: 1.4;
        }
        
        h6 {
            font-size: 1rem;
            line-height: 1.5;
        }
        
        p {
            margin: 0 0 var(--spacing-4) 0;
            color: var(--color-neutral-700);
        }
        
        /* GLASSMORPHISM */
        .glass {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border-radius: var(--radius-xl);
            border: var(--glass-border);
            box-shadow: var(--shadow-lg);
        }
        
        .glass-dark {
            background: rgba(17, 24, 39, 0.8);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border-radius: var(--radius-xl);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: var(--shadow-lg);
            color: white;
        }
        
        /* NEUMORPHISM */
        .neumorph {
            background: var(--color-neutral-100);
            border-radius: var(--radius-xl);
            box-shadow: 
                8px 8px 16px rgba(200, 200, 200, 0.4), 
                -8px -8px 16px rgba(255, 255, 255, 0.8);
        }
        
        .neumorph-inset {
            background: var(--color-neutral-100);
            border-radius: var(--radius-xl);
            box-shadow: 
                inset 8px 8px 16px rgba(200, 200, 200, 0.4), 
                inset -8px -8px 16px rgba(255, 255, 255, 0.8);
        }
        
        /* STREAMLIT COMPONENT OVERRIDES */
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: var(--glass-gradient-blue);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border-right: var(--glass-border);
        }
        
        section[data-testid="stSidebar"] .sidebar-content {
            color: white;
        }
        
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Buttons */
        .stButton > button {
            font-family: var(--font-body);
            font-weight: 500;
            background: var(--gradient-blue);
            color: white;
            border: none;
            border-radius: var(--radius-xl);
            padding: var(--spacing-3) var(--spacing-6);
            cursor: pointer;
            transition: all var(--duration-300) var(--ease-out);
            box-shadow: var(--shadow-blue-sm);
            height: auto;
            min-height: 2.5rem;
            line-height: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--spacing-2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-blue-md);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: var(--shadow-blue-sm);
        }
        
        /* Secondary button style */
        .btn-secondary > button {
            background: var(--color-neutral-100);
            color: var(--color-neutral-800);
            border: 1px solid var(--color-neutral-200);
            box-shadow: var(--shadow-md);
        }
        
        .btn-secondary > button:hover {
            background: var(--color-neutral-50);
            box-shadow: var(--shadow-lg);
        }
        
        /* Tertiary button - minimal style */
        .btn-tertiary > button {
            background: transparent;
            color: var(--color-primary-500);
            border: none;
            box-shadow: none;
        }
        
        .btn-tertiary > button:hover {
            background: var(--color-primary-50);
            transform: none;
            box-shadow: none;
        }
        
        /* Success button */
        .btn-success > button {
            background: var(--gradient-success);
            box-shadow: var(--shadow-md);
        }
        
        .btn-success > button:hover {
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }
        
        /* Warning button */
        .btn-warning > button {
            background: var(--gradient-warning);
            box-shadow: var(--shadow-md);
        }
        
        .btn-warning > button:hover {
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
        }
        
        /* Error button */
        .btn-error > button {
            background: var(--gradient-error);
            box-shadow: var(--shadow-md);
        }
        
        .btn-error > button:hover {
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        }
        
        /* Icon Button */
        .btn-icon > button {
            padding: var(--spacing-2);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Input fields */
        div[data-baseweb="input"] {
            border-radius: var(--radius-lg);
            transition: all var(--duration-200) var(--ease-out);
            overflow: hidden;
        }
        
        div[data-baseweb="input"] input {
            border-radius: var(--radius-lg);
            border: 1px solid var(--color-neutral-200);
            padding: var(--spacing-3) var(--spacing-4);
            font-family: var(--font-body);
            font-size: 0.9rem;
            transition: all var(--duration-200) var(--ease-out);
            box-shadow: var(--shadow-sm);
        }
        
        div[data-baseweb="input"] input:focus {
            border-color: var(--color-primary-500);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }
        
        /* Select boxes */
        div[data-baseweb="select"] {
            border-radius: var(--radius-lg);
            transition: all var(--duration-200) var(--ease-out);
            overflow: hidden;
        }
        
        div[data-baseweb="select"] > div {
            border-radius: var(--radius-lg);
            border: 1px solid var(--color-neutral-200);
            font-family: var(--font-body);
            transition: all var(--duration-200) var(--ease-out);
            box-shadow: var(--shadow-sm);
        }
        
        div[data-baseweb="select"] > div:hover {
            border-color: var(--color-neutral-300);
            box-shadow: var(--shadow-md);
        }
        
        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--color-primary-500);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }
        
        /* Multiselect */
        div[data-baseweb="select"] [role="listbox"] {
            background: white;
            border-radius: var(--radius-lg);
            border: 1px solid var(--color-neutral-200);
            box-shadow: var(--shadow-xl);
        }
        
        div[data-baseweb="select"] [role="option"] {
            font-family: var(--font-body);
            transition: all var(--duration-100) var(--ease-out);
        }
        
        div[data-baseweb="select"] [role="option"]:hover {
            background: var(--color-primary-50);
        }
        
        /* Checkbox */
        label[data-baseweb="checkbox"] {
            font-family: var(--font-body);
            gap: var(--spacing-3);
        }
        
        /* Radio buttons */
        div[role="radiogroup"] {
            margin: var(--spacing-4) 0;
        }
        
        div[role="radiogroup"] label {
            font-family: var(--font-body);
            padding: var(--spacing-2) var(--spacing-4);
            border-radius: var(--radius-lg);
            transition: all var(--duration-200) var(--ease-out);
        }
        
        div[role="radiogroup"] label:hover {
            background: var(--color-neutral-100);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: var(--spacing-2);
            border-bottom: 1px solid var(--color-neutral-200);
            margin-bottom: var(--spacing-4);
            padding-bottom: var(--spacing-2);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            padding: var(--spacing-3) var(--spacing-5);
            font-family: var(--font-body);
            font-weight: 500;
            color: var(--color-neutral-600);
            transition: all var(--duration-200) var(--ease-out);
            border: none;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--color-primary-500);
            background: rgba(59, 130, 246, 0.05);
        }
        
        .stTabs [aria-selected="true"] {
            color: var(--color-primary-600) !important;
            font-weight: 600 !important;
            background: rgba(59, 130, 246, 0.1) !important;
            border-bottom: 2px solid var(--color-primary-500) !important;
        }
        
        /* Metrics */
        div[data-testid="stMetricValue"] {
            font-family: var(--font-heading);
            font-weight: 700;
            color: var(--color-primary-600);
            font-size: 1.75rem;
        }
        
        div[data-testid="stMetricLabel"] {
            font-family: var(--font-body);
            color: var(--color-neutral-600);
            font-weight: 500;
        }
        
        /* Expanders */
        [data-testid="stExpander"] {
            border: 1px solid var(--color-neutral-200);
            border-radius: var(--radius-xl);
            overflow: hidden;
            transition: all var(--duration-300) var(--ease-out);
            box-shadow: var(--shadow-sm);
            margin-bottom: var(--spacing-4);
        }
        
        [data-testid="stExpander"]:hover {
            box-shadow: var(--shadow-md);
        }
        
        [data-testid="stExpander"] > div:first-child {
            background: var(--color-neutral-50);
            padding: var(--spacing-4);
            border-bottom: 1px solid var(--color-neutral-200);
        }
        
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            padding: var(--spacing-4);
        }
        
        /* CUSTOM COMPONENTS */
        /* Card */
        .card {
            background: white;
            border-radius: var(--radius-xl);
            padding: var(--spacing-6);
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            position: relative;
            overflow: hidden;
            margin-bottom: var(--spacing-6);
        }
        
        .card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .card-interactive {
            cursor: pointer;
        }
        
        .card-title {
            font-family: var(--font-heading);
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: var(--spacing-4);
            color: var(--color-neutral-900);
            position: relative;
            z-index: 1;
        }
        
        .card-title::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            height: 3px;
            width: 40px;
            border-radius: var(--radius-full);
            background: var(--gradient-blue);
        }
        
        .card-content {
            position: relative;
            z-index: 1;
        }
        
        .card-glass {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border: var(--glass-border);
        }
        
        .card-glass-dark {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: white;
        }
        
        .card-glass-dark .card-title {
            color: white;
        }
        
        .card-gradient-blue {
            background: var(--gradient-blue);
            color: white;
        }
        
        .card-gradient-blue .card-title {
            color: white;
        }
        
        .card-gradient-blue .card-title::after {
            background: white;
        }
        
        .card-gradient-purple {
            background: var(--gradient-purple);
            color: white;
        }
        
        .card-gradient-purple .card-title {
            color: white;
        }
        
        .card-gradient-purple .card-title::after {
            background: white;
        }
        
        .card-gradient-pink {
            background: var(--gradient-pink);
            color: white;
        }
        
        .card-gradient-pink .card-title {
            color: white;
        }
        
        .card-gradient-pink .card-title::after {
            background: white;
        }
        
        /* 3D Card Effect */
        .card-3d {
            transition: transform 0.5s var(--ease-out);
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .card-3d:hover {
            transform: rotateX(5deg) rotateY(5deg) translateZ(10px);
        }
        
        /* Card with decorative shapes */
        .card-decorative::before {
            content: '';
            position: absolute;
            top: -100px;
            right: -100px;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: var(--color-primary-100);
            z-index: 0;
            opacity: 0.6;
        }
        
        .card-decorative::after {
            content: '';
            position: absolute;
            bottom: -80px;
            left: 20%;
            width: 150px;
            height: 150px;
            border-radius: var(--radius-2xl);
            background: var(--color-secondary-100);
            transform: rotate(45deg);
            z-index: 0;
            opacity: 0.5;
        }
        
        /* Card with border glow */
        .card-glow {
            border: 1px solid transparent;
            background-clip: padding-box;
            position: relative;
        }
        
        .card-glow::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: var(--radius-xl); 
            padding: 2px; 
            background: var(--gradient-blue-purple);
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }
        
        .card-glow:hover::before {
            background: var(--gradient-purple-pink);
        }
        
        /* Badge */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: var(--spacing-1) var(--spacing-3);
            border-radius: var(--radius-full);
            font-family: var(--font-sans);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }
        
        .badge-primary {
            background: var(--color-primary-100);
            color: var(--color-primary-700);
        }
        
        .badge-secondary {
            background: var(--color-secondary-100);
            color: var(--color-secondary-700);
        }
        
        .badge-tertiary {
            background: var(--color-tertiary-100);
            color: var(--color-tertiary-700);
        }
        
        .badge-success {
            background: var(--color-success-100);
            color: var(--color-success-700);
        }
        
        .badge-warning {
            background: var(--color-warning-100);
            color: var(--color-warning-700);
        }
        
        .badge-error {
            background: var(--color-error-100);
            color: var(--color-error-700);
        }
        
        /* Pill badge with gradient */
        .badge-pill {
            border-radius: var(--radius-full);
            padding: var(--spacing-1) var(--spacing-4);
        }
        
        .badge-gradient-blue {
            background: var(--gradient-blue);
            color: white;
        }
        
        .badge-gradient-purple {
            background: var(--gradient-purple);
            color: white;
        }
        
        .badge-gradient-pink {
            background: var(--gradient-pink);
            color: white;
        }
        
        /* Avatar */
        .avatar {
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-sans);
            font-weight: 600;
            background: var(--gradient-blue);
            color: white;
            position: relative;
        }
        
        .avatar-sm {
            width: 32px;
            height: 32px;
            font-size: 0.75rem;
        }
        
        .avatar-md {
            width: 40px;
            height: 40px;
            font-size: 0.875rem;
        }
        
        .avatar-lg {
            width: 56px;
            height: 56px;
            font-size: 1.125rem;
        }
        
        .avatar-xl {
            width: 80px;
            height: 80px;
            font-size: 1.5rem;
        }
        
        .avatar-2xl {
            width: 120px;
            height: 120px;
            font-size: 2rem;
        }
        
        .avatar-gradient-blue {
            background: var(--gradient-blue);
        }
        
        .avatar-gradient-purple {
            background: var(--gradient-purple);
        }
        
        .avatar-gradient-pink {
            background: var(--gradient-pink);
        }
        
        .avatar-border {
            border: 3px solid white;
            box-shadow: var(--shadow-md);
        }
        
        .avatar-group {
            display: inline-flex;
        }
        
        .avatar-group .avatar {
            margin-left: -10px;
            border: 2px solid white;
            box-shadow: var(--shadow-sm);
            transition: transform var(--duration-300) var(--ease-out);
        }
        
        .avatar-group .avatar:first-child {
            margin-left: 0;
        }
        
        .avatar-group:hover .avatar {
            transform: translateX(0);
        }
        
        .avatar-group .avatar:hover {
            z-index: 1;
            transform: scale(1.1) !important;
        }
        
        /* Avatar with status indicator */
        .avatar-status::after {
            content: '';
            position: absolute;
            bottom: 0;
            right: 0;
            width: 25%;
            height: 25%;
            border-radius: 50%;
            background: var(--color-success-500);
            border: 2px solid white;
        }
        
        .avatar-status-online::after {
            background: var(--color-success-500);
        }
        
        .avatar-status-away::after {
            background: var(--color-warning-500);
        }
        
        .avatar-status-busy::after {
            background: var(--color-error-500);
        }
        
        .avatar-status-offline::after {
            background: var(--color-neutral-400);
        }
        
        /* Button Group */
        .button-group {
            display: inline-flex;
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }
        
        .button-group button {
            border: none;
            background: var(--color-neutral-100);
            color: var(--color-neutral-700);
            padding: var(--spacing-2) var(--spacing-4);
            font-family: var(--font-body);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--duration-200) var(--ease-out);
        }
        
        .button-group button:hover {
            background: var(--color-neutral-200);
        }
        
        .button-group button.active {
            background: var(--color-primary-500);
            color: white;
        }
        
        .button-group button:not(:last-child) {
            border-right: 1px solid var(--color-neutral-200);
        }
        
        /* Progress bar */
        .progress {
            height: 8px;
            border-radius: var(--radius-full);
            background: var(--color-neutral-200);
            overflow: hidden;
            position: relative;
        }
        
        .progress-bar {
            height: 100%;
            background: var(--gradient-blue);
            border-radius: var(--radius-full);
            transition: width var(--duration-500) var(--ease-out);
        }
        
        .progress-bar-striped {
            background-image: linear-gradient(
                45deg,
                rgba(255, 255, 255, 0.15) 25%,
                transparent 25%,
                transparent 50%,
                rgba(255, 255, 255, 0.15) 50%,
                rgba(255, 255, 255, 0.15) 75%,
                transparent 75%,
                transparent
            );
            background-size: 1rem 1rem;
        }
        
        .progress-sm {
            height: 4px;
        }
        
        .progress-lg {
            height: 12px;
        }
        
        .progress-xl {
            height: 16px;
        }
        
        /* Form elements */
        .form-group {
            margin-bottom: var(--spacing-5);
        }
        
        .form-label {
            display: block;
            margin-bottom: var(--spacing-2);
            font-weight: 500;
            color: var(--color-neutral-700);
        }
        
        .form-control {
            width: 100%;
            padding: var(--spacing-3) var(--spacing-4);
            border-radius: var(--radius-lg);
            border: 1px solid var(--color-neutral-200);
            background: white;
            font-family: var(--font-body);
            font-size: 0.9rem;
            transition: all var(--duration-200) var(--ease-out);
            box-shadow: var(--shadow-sm);
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--color-primary-500);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .form-description {
            margin-top: var(--spacing-1);
            font-size: 0.8rem;
            color: var(--color-neutral-500);
        }
        
        .form-error {
            margin-top: var(--spacing-1);
            font-size: 0.8rem;
            color: var(--color-error-500);
        }
        
        /* Stat card */
        .stat-card {
            display: flex;
            align-items: center;
            padding: var(--spacing-5);
            background: white;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: var(--radius-xl);
            background: var(--color-primary-100);
            color: var(--color-primary-600);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-right: var(--spacing-4);
            flex-shrink: 0;
        }
        
        .stat-icon-rounded {
            border-radius: 50%;
        }
        
        .stat-icon-gradient {
            background: var(--gradient-blue);
            color: white;
        }
        
        .stat-content {
            flex-grow: 1;
        }
        
        .stat-value {
            font-family: var(--font-heading);
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--color-neutral-900);
            line-height: 1.2;
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: var(--color-neutral-500);
            margin-top: var(--spacing-1);
        }
        
        .stat-change {
            display: flex;
            align-items: center;
            font-size: 0.875rem;
            font-weight: 500;
            margin-top: var(--spacing-1);
        }
        
        .stat-change-positive {
            color: var(--color-success-500);
        }
        
        .stat-change-negative {
            color: var(--color-error-500);
        }
        
        /* Charts and graph styles */
        .chart-container {
            background: white;
            border-radius: var(--radius-xl);
            padding: var(--spacing-5);
            box-shadow: var(--shadow-md);
            margin-bottom: var(--spacing-6);
        }
        
        .chart-title {
            font-family: var(--font-heading);
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--color-neutral-800);
            margin-bottom: var(--spacing-4);
        }
        
        .chart-content {
            position: relative;
            height: 300px;
        }
        
        /* Data grid */
        .data-grid {
            border-collapse: collapse;
            width: 100%;
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            font-family: var(--font-body);
        }
        
        .data-grid th {
            background: var(--color-neutral-100);
            padding: var(--spacing-3) var(--spacing-4);
            text-align: left;
            font-weight: 600;
            color: var(--color-neutral-700);
            border-bottom: 1px solid var(--color-neutral-200);
        }
        
        .data-grid td {
            padding: var(--spacing-3) var(--spacing-4);
            border-bottom: 1px solid var(--color-neutral-200);
            color: var(--color-neutral-700);
        }
        
        .data-grid tr:last-child td {
            border-bottom: none;
        }
        
        .data-grid tr:hover td {
            background: var(--color-neutral-50);
        }
        
        /* Timeline */
        .timeline {
            position: relative;
            padding-left: var(--spacing-8);
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            width: 2px;
            background: var(--color-neutral-200);
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: var(--spacing-6);
        }
        
        .timeline-dot {
            position: absolute;
            top: 4px;
            left: calc(-1 * var(--spacing-8) + 1px);
            transform: translateX(-50%);
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--color-primary-500);
            border: 3px solid white;
            box-shadow: var(--shadow-md);
            z-index: 1;
        }
        
        .timeline-content {
            background: white;
            border-radius: var(--radius-lg);
            padding: var(--spacing-4);
            box-shadow: var(--shadow-md);
        }
        
        .timeline-date {
            font-size: 0.875rem;
            color: var(--color-neutral-500);
            margin-bottom: var(--spacing-2);
        }
        
        .timeline-title {
            font-weight: 600;
            margin-bottom: var(--spacing-2);
        }
        
        .timeline-body {
            color: var(--color-neutral-600);
        }
        
        /* Activity item */
        .activity-item {
            display: flex;
            padding: var(--spacing-4);
            background: white;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            margin-bottom: var(--spacing-4);
            transition: all var(--duration-300) var(--ease-out);
        }
        
        .activity-item:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .activity-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--color-primary-100);
            color: var(--color-primary-600);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-right: var(--spacing-4);
            flex-shrink: 0;
        }
        
        .activity-content {
            flex-grow: 1;
        }
        
        .activity-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-2);
        }
        
        .activity-user {
            font-weight: 600;
            color: var(--color-neutral-800);
        }
        
        .activity-time {
            font-size: 0.75rem;
            color: var(--color-neutral-500);
        }
        
        .activity-description {
            color: var(--color-neutral-600);
            margin-bottom: var(--spacing-2);
        }
        
        .activity-actions {
            display: flex;
            gap: var(--spacing-2);
            margin-top: var(--spacing-2);
        }
        
        /* Notifications */
        .notification-item {
            display: flex;
            padding: var(--spacing-4);
            background: white;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            margin-bottom: var(--spacing-4);
            transition: all var(--duration-300) var(--ease-out);
            border-left: 3px solid transparent;
        }
        
        .notification-item:hover {
            transform: translateX(4px);
            box-shadow: var(--shadow-lg);
        }
        
        .notification-item.unread {
            border-left-color: var(--color-primary-500);
            background: var(--color-primary-50);
        }
        
        .notification-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--color-primary-100);
            color: var(--color-primary-600);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-right: var(--spacing-4);
            flex-shrink: 0;
        }
        
        .notification-content {
            flex-grow: 1;
        }
        
        .notification-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-2);
        }
        
        .notification-title {
            font-weight: 600;
            color: var(--color-neutral-800);
        }
        
        .notification-time {
            font-size: 0.75rem;
            color: var(--color-neutral-500);
        }
        
        .notification-body {
            color: var(--color-neutral-600);
            margin-bottom: var(--spacing-2);
        }
        
        .notification-actions {
            display: flex;
            gap: var(--spacing-2);
            margin-top: var(--spacing-2);
        }
        
        /* Animation utilities */
        .animate-fade-in {
            animation: fadeIn var(--duration-500) var(--ease-out) forwards;
        }
        
        .animate-slide-up {
            animation: slideUp var(--duration-500) var(--ease-out) forwards;
        }
        
        .animate-slide-right {
            animation: slideRight var(--duration-500) var(--ease-out) forwards;
        }
        
        .animate-scale {
            animation: scale var(--duration-500) var(--ease-out) forwards;
        }
        
        .animate-pulse {
            animation: pulse 2s var(--ease-in-out) infinite;
        }
        
        .animate-bounce {
            animation: bounce 1s var(--ease-in-out) infinite;
        }
        
        .animate-spin {
            animation: spin 1s linear infinite;
        }
        
        .animate-delay-100 {
            animation-delay: 100ms;
        }
        
        .animate-delay-200 {
            animation-delay: 200ms;
        }
        
        .animate-delay-300 {
            animation-delay: 300ms;
        }
        
        .animate-delay-400 {
            animation-delay: 400ms;
        }
        
        .animate-delay-500 {
            animation-delay: 500ms;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideRight {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes scale {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* Event card */
        .event-card {
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .event-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .event-card:hover .event-image img {
            transform: scale(1.05);
        }
        
        .event-image {
            height: 180px;
            overflow: hidden;
            position: relative;
        }
        
        .event-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--duration-500) var(--ease-out);
        }
        
        .event-date-badge {
            position: absolute;
            top: var(--spacing-4);
            right: var(--spacing-4);
            background: white;
            color: var(--color-neutral-800);
            padding: var(--spacing-2) var(--spacing-3);
            border-radius: var(--radius-lg);
            font-weight: 600;
            font-size: 0.875rem;
            box-shadow: var(--shadow-md);
            z-index: 1;
        }
        
        .event-content {
            padding: var(--spacing-5);
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .event-meta {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
            margin-bottom: var(--spacing-3);
        }
        
        .event-category {
            color: var(--color-primary-600);
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .event-time {
            color: var(--color-neutral-600);
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: var(--spacing-1);
        }
        
        .event-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--color-neutral-900);
            margin-bottom: var(--spacing-3);
            line-height: 1.4;
        }
        
        .event-description {
            color: var(--color-neutral-600);
            font-size: 0.875rem;
            margin-bottom: var(--spacing-4);
            line-height: 1.6;
        }
        
        .event-footer {
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: var(--spacing-4);
            border-top: 1px solid var(--color-neutral-200);
        }
        
        .event-location {
            display: flex;
            align-items: center;
            gap: var(--spacing-2);
            color: var(--color-neutral-600);
            font-size: 0.875rem;
        }
        
        .event-attendees {
            display: flex;
            align-items: center;
            gap: var(--spacing-2);
            color: var(--color-neutral-600);
            font-size: 0.875rem;
        }
        
        /* Circle card */
        .circle-card {
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .circle-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .circle-banner {
            height: 80px;
            background: var(--gradient-blue);
            position: relative;
        }
        
        .circle-avatar {
            position: absolute;
            bottom: 0;
            left: var(--spacing-5);
            transform: translateY(50%);
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.5rem;
            color: var(--color-primary-600);
            border: 3px solid white;
            box-shadow: var(--shadow-md);
        }
        
        .circle-content {
            padding: var(--spacing-5);
            padding-top: calc(64px / 2 + var(--spacing-4));
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .circle-title {
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: var(--spacing-2);
            color: var(--color-neutral-900);
        }
        
        .circle-description {
            font-size: 0.875rem;
            color: var(--color-neutral-600);
            margin-bottom: var(--spacing-4);
            line-height: 1.6;
        }
        
        .circle-stats {
            display: flex;
            gap: var(--spacing-6);
            margin-bottom: var(--spacing-4);
        }
        
        .circle-stat {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .circle-stat-value {
            font-weight: 700;
            color: var(--color-neutral-900);
            font-size: 1.125rem;
        }
        
        .circle-stat-label {
            font-size: 0.75rem;
            color: var(--color-neutral-500);
        }
        
        .circle-tags {
            display: flex;
            flex-wrap: wrap;
            gap: var(--spacing-2);
            margin-bottom: var(--spacing-4);
        }
        
        .circle-footer {
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: var(--spacing-4);
            border-top: 1px solid var(--color-neutral-200);
        }
        
        .circle-privacy {
            font-size: 0.75rem;
            color: var(--color-neutral-500);
            display: flex;
            align-items: center;
            gap: var(--spacing-1);
        }
        
        /* Media gallery */
        .gallery-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: var(--spacing-4);
            margin-bottom: var(--spacing-6);
        }
        
        .gallery-item {
            position: relative;
            border-radius: var(--radius-lg);
            overflow: hidden;
            aspect-ratio: 1;
            box-shadow: var(--shadow-md);
            cursor: pointer;
            transition: all var(--duration-300) var(--ease-out);
        }
        
        .gallery-item:hover {
            transform: scale(1.02);
            box-shadow: var(--shadow-lg);
            z-index: 1;
        }
        
        .gallery-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform var(--duration-500) var(--ease-out);
        }
        
        .gallery-item:hover .gallery-image {
            transform: scale(1.1);
        }
        
        .gallery-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: var(--spacing-4);
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            color: white;
            opacity: 0;
            transform: translateY(10px);
            transition: all var(--duration-300) var(--ease-out);
        }
        
        .gallery-item:hover .gallery-overlay {
            opacity: 1;
            transform: translateY(0);
        }
        
        .gallery-title {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: var(--spacing-1);
        }
        
        .gallery-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            opacity: 0.8;
        }
        
        /* Masonry gallery layout */
        @media (min-width: 768px) {
            .gallery-masonry {
                column-count: 3;
                column-gap: var(--spacing-4);
            }
            
            .gallery-masonry .gallery-item {
                break-inside: avoid;
                margin-bottom: var(--spacing-4);
                height: auto;
                aspect-ratio: unset;
            }
        }
        
        /* Business card */
        .business-card {
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .business-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .business-header {
            display: flex;
            padding: var(--spacing-5);
            border-bottom: 1px solid var(--color-neutral-200);
        }
        
        .business-logo {
            width: 64px;
            height: 64px;
            border-radius: var(--radius-lg);
            object-fit: cover;
            margin-right: var(--spacing-4);
            border: 1px solid var(--color-neutral-200);
            flex-shrink: 0;
        }
        
        .business-info {
            flex-grow: 1;
        }
        
        .business-name {
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: var(--spacing-1);
            color: var(--color-neutral-900);
            display: flex;
            align-items: center;
            gap: var(--spacing-2);
        }
        
        .business-verified-badge {
            color: var(--color-primary-600);
            font-size: 1rem;
        }
        
        .business-category {
            font-size: 0.875rem;
            color: var(--color-primary-600);
            margin-bottom: var(--spacing-2);
        }
        
        .business-meta {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
            font-size: 0.75rem;
            color: var(--color-neutral-500);
        }
        
        .business-body {
            padding: var(--spacing-5);
            flex-grow: 1;
        }
        
        .business-section {
            margin-bottom: var(--spacing-5);
        }
        
        .business-section:last-child {
            margin-bottom: 0;
        }
        
        .business-section-title {
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--color-neutral-500);
            margin-bottom: var(--spacing-3);
        }
        
        .business-description {
            font-size: 0.875rem;
            color: var(--color-neutral-700);
            margin-bottom: var(--spacing-3);
            line-height: 1.6;
        }
        
        .business-location {
            display: flex;
            align-items: center;
            gap: var(--spacing-2);
            font-size: 0.875rem;
            color: var(--color-neutral-700);
            margin-bottom: var(--spacing-2);
        }
        
        .business-hours {
            font-size: 0.875rem;
            color: var(--color-neutral-700);
        }
        
        .business-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-5);
            border-top: 1px solid var(--color-neutral-200);
        }
        
        .business-rating {
            display: flex;
            align-items: center;
            gap: var(--spacing-1);
            font-weight: 600;
            color: var(--color-neutral-900);
        }
        
        .business-rating-stars {
            color: var(--color-warning-500);
            letter-spacing: -0.1em;
        }
        
        .business-reviews {
            font-size: 0.75rem;
            color: var(--color-neutral-500);
        }
        
        /* Promotion card */
        .promotion-card {
            background: white;
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 1;
        }
        
        .promotion-card:hover {
            transform: translateY(-5px) translateZ(0);
            box-shadow: var(--shadow-lg);
        }
        
        .promotion-header {
            position: relative;
            padding: var(--spacing-5);
            background: var(--gradient-purple-pink);
            color: white;
            overflow: hidden;
        }
        
        .promotion-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 50%);
            opacity: 0;
            transition: opacity var(--duration-500) var(--ease-out);
            z-index: 0;
        }
        
        .promotion-card:hover .promotion-header::before {
            opacity: 1;
        }
        
        .promotion-title {
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: var(--spacing-1);
            position: relative;
            z-index: 1;
        }
        
        .promotion-subtitle {
            font-size: 0.875rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .promotion-offer {
            position: absolute;
            top: var(--spacing-4);
            right: var(--spacing-4);
            background: white;
            color: var(--color-neutral-900);
            border-radius: var(--radius-full);
            padding: var(--spacing-1) var(--spacing-3);
            font-weight: 600;
            font-size: 0.75rem;
            z-index: 1;
        }
        
        .promotion-body {
            padding: var(--spacing-5);
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .promotion-description {
            font-size: 0.875rem;
            color: var(--color-neutral-700);
            margin-bottom: var(--spacing-4);
            line-height: 1.6;
        }
        
        .promotion-requirements {
            background: var(--color-neutral-50);
            border-radius: var(--radius-lg);
            padding: var(--spacing-3);
            font-size: 0.8125rem;
            color: var(--color-neutral-700);
            margin-bottom: var(--spacing-4);
        }
        
        .promotion-requirements-title {
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: var(--spacing-2);
            color: var(--color-neutral-900);
        }
        
        .promotion-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
        }
        
        .promotion-meta {
            display: flex;
            flex-direction: column;
        }
        
        .promotion-expiry {
            font-size: 0.75rem;
            color: var(--color-neutral-500);
        }
        
        .promotion-claimed {
            font-size: 0.75rem;
            color: var(--color-primary-600);
            font-weight: 500;
        }
        
        /* Auth container */
        .auth-container {
            max-width: 420px;
            margin: 2rem auto;
            padding: var(--spacing-6);
            background: white;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }
        
        .auth-container::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 150px;
            height: 150px;
            background: var(--color-primary-100);
            border-radius: 50%;
            transform: translate(30%, -30%);
            z-index: 0;
        }
        
        .auth-container::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 150px;
            height: 150px;
            background: var(--color-secondary-100);
            border-radius: 50%;
            transform: translate(-30%, 30%);
            z-index: 0;
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: var(--spacing-6);
            position: relative;
            z-index: 1;
        }
        
        .auth-logo {
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-primary-600);
            margin-bottom: var(--spacing-1);
            display: inline-block;
            position: relative;
        }
        
        .auth-logo::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-blue-purple);
            border-radius: var(--radius-full);
        }
        
        .auth-subtitle {
            font-size: 0.9rem;
            color: var(--color-neutral-600);
        }
        
        .auth-form {
            position: relative;
            z-index: 1;
        }
        
        .auth-input {
            width: 100%;
            padding: var(--spacing-3) var(--spacing-4);
            border-radius: var(--radius-lg);
            border: 1px solid var(--color-neutral-200);
            background: white;
            font-family: var(--font-body);
            font-size: 0.9rem;
            margin-bottom: var(--spacing-4);
            transition: all var(--duration-200) var(--ease-out);
            box-shadow: var(--shadow-sm);
        }
        
        .auth-input:focus {
            outline: none;
            border-color: var(--color-primary-500);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        
        .auth-button {
            width: 100%;
            padding: var(--spacing-3) var(--spacing-4);
            background: var(--gradient-blue);
            color: white;
            border: none;
            border-radius: var(--radius-lg);
            font-family: var(--font-body);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--duration-200) var(--ease-out);
            box-shadow: var(--shadow-md);
            margin-bottom: var(--spacing-4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--spacing-2);
        }
        
        .auth-button:hover {
            box-shadow: var(--shadow-blue-md);
            transform: translateY(-2px);
        }
        
        .auth-button:active {
            transform: translateY(0);
            box-shadow: var(--shadow-md);
        }
        
        .auth-button-social {
            width: 100%;
            padding: var(--spacing-3) var(--spacing-4);
            background: white;
            color: var(--color-neutral-700);
            border: 1px solid var(--color-neutral-200);
            border-radius: var(--radius-lg);
            font-family: var(--font-body);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--duration-200) var(--ease-out);
            box-shadow: var(--shadow-sm);
            margin-bottom: var(--spacing-4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--spacing-3);
        }
        
        .auth-button-social:hover {
            background: var(--color-neutral-50);
            box-shadow: var(--shadow-md);
        }
        
        .auth-button-social.google {
            color: #4285F4;
        }
        
        .auth-button-social.facebook {
            color: #1877F2;
        }
        
        .auth-button-social.apple {
            color: #000000;
        }
        
        .auth-separator {
            display: flex;
            align-items: center;
            text-align: center;
            margin: var(--spacing-5) 0;
            color: var(--color-neutral-500);
            font-size: 0.875rem;
            position: relative;
            z-index: 1;
        }
        
        .auth-separator::before,
        .auth-separator::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid var(--color-neutral-200);
        }
        
        .auth-separator::before {
            margin-right: var(--spacing-3);
        }
        
        .auth-separator::after {
            margin-left: var(--spacing-3);
        }
        
        .auth-footer {
            text-align: center;
            margin-top: var(--spacing-5);
            font-size: 0.875rem;
            color: var(--color-neutral-600);
            position: relative;
            z-index: 1;
        }
        
        .auth-link {
            color: var(--color-primary-600);
            font-weight: 500;
            text-decoration: none;
            transition: color var(--duration-200) var(--ease-out);
        }
        
        .auth-link:hover {
            color: var(--color-primary-700);
            text-decoration: underline;
        }
        
        /* Welcome landing page */
        .welcome-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--spacing-6);
        }
        
        .welcome-hero {
            display: flex;
            align-items: center;
            margin-bottom: var(--spacing-16);
            position: relative;
        }
        
        .welcome-hero::before {
            content: '';
            position: absolute;
            top: -150px;
            right: -150px;
            width: 300px;
            height: 300px;
            background: var(--color-primary-100);
            border-radius: 50%;
            opacity: 0.5;
            z-index: -1;
        }
        
        .welcome-hero::after {
            content: '';
            position: absolute;
            bottom: -150px;
            left: -150px;
            width: 300px;
            height: 300px;
            background: var(--color-secondary-100);
            border-radius: 50%;
            opacity: 0.5;
            z-index: -1;
        }
        
        .welcome-content {
            flex: 1;
            padding-right: var(--spacing-10);
            position: relative;
            z-index: 1;
        }
        
        .welcome-title {
            font-family: var(--font-heading);
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: var(--spacing-6);
            color: var(--color-neutral-900);
            position: relative;
        }
        
        .welcome-title span {
            display: inline-block;
            position: relative;
            color: var(--color-primary-600);
        }
        
        .welcome-title span::before {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: var(--gradient-blue);
            border-radius: var(--radius-full);
            opacity: 0.3;
        }
        
        .welcome-subtitle {
            font-size: 1.25rem;
            color: var(--color-neutral-600);
            margin-bottom: var(--spacing-8);
            line-height: 1.5;
            max-width: 80%;
        }
        
        .welcome-image {
            flex: 1;
            position: relative;
            z-index: 1;
        }
        
        .welcome-image img {
            max-width: 100%;
            border-radius: var(--radius-2xl);
            box-shadow: var(--shadow-xl);
            transform: perspective(1000px) rotateY(-5deg) rotateX(5deg) translateZ(20px);
            transition: all var(--duration-500) var(--ease-out);
        }
        
        .welcome-image:hover img {
            transform: perspective(1000px) rotateY(-2deg) rotateX(2deg) translateZ(30px);
            box-shadow: var(--shadow-2xl);
        }
        
        .welcome-cta {
            display: flex;
            gap: var(--spacing-4);
        }
        
        .welcome-button {
            padding: var(--spacing-3) var(--spacing-6);
            border-radius: var(--radius-lg);
            font-family: var(--font-body);
            font-weight: 500;
            font-size: 1rem;
            transition: all var(--duration-300) var(--ease-out);
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-2);
            cursor: pointer;
        }
        
        .welcome-button-primary {
            background: var(--gradient-blue);
            color: white;
            border: none;
            box-shadow: var(--shadow-blue-sm);
        }
        
        .welcome-button-primary:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-blue-md);
        }
        
        .welcome-button-secondary {
            background: white;
            color: var(--color-primary-600);
            border: 1px solid var(--color-primary-200);
            box-shadow: var(--shadow-sm);
        }
        
        .welcome-button-secondary:hover {
            background: var(--color-primary-50);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .welcome-features {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--spacing-8);
            margin-bottom: var(--spacing-16);
        }
        
        .feature-card {
            background: white;
            border-radius: var(--radius-xl);
            padding: var(--spacing-6);
            box-shadow: var(--shadow-md);
            transition: all var(--duration-300) var(--ease-out);
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-blue);
            z-index: 0;
        }
        
        .feature-card:nth-child(2)::before {
            background: var(--gradient-purple);
        }
        
        .feature-card:nth-child(3)::before {
            background: var(--gradient-pink);
        }
        
        .feature-icon {
            width: 56px;
            height: 56px;
            border-radius: var(--radius-lg);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: var(--spacing-4);
            background: var(--color-primary-100);
            color: var(--color-primary-600);
            position: relative;
            z-index: 1;
        }
        
        .feature-card:nth-child(2) .feature-icon {
            background: var(--color-secondary-100);
            color: var(--color-secondary-600);
        }
        
        .feature-card:nth-child(3) .feature-icon {
            background: var(--color-tertiary-100);
            color: var(--color-tertiary-600);
        }
        
        .feature-title {
            font-family: var(--font-heading);
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: var(--spacing-3);
            color: var(--color-neutral-900);
            position: relative;
            z-index: 1;
        }
        
        .feature-description {
            color: var(--color-neutral-700);
            font-size: 0.9rem;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }
        
        /* Responsive adjustments */
        @media (max-width: 1024px) {
            .welcome-title {
                font-size: 3rem;
            }
            
            .welcome-subtitle {
                font-size: 1.125rem;
                max-width: 100%;
            }
        }
        
        @media (max-width: 768px) {
            .welcome-hero {
                flex-direction: column;
            }
            
            .welcome-content {
                padding-right: 0;
                margin-bottom: var(--spacing-8);
            }
            
            .welcome-title {
                font-size: 2.5rem;
            }
            
            .welcome-features {
                grid-template-columns: 1fr;
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            /* Base dark mode styles would go here */
            /* For simplicity, we're not implementing full dark mode in this example */
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

def get_random_placeholder_image(seed, width=800, height=600):
    """Get a random placeholder image URL with a seed for consistency"""
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"

# Component rendering functions
def render_card(title, content, footer=None, badge=None, card_class="", card_style=""):
    """Render a card with title and content"""
    badge_html = f'<div class="badge badge-primary">{badge}</div>' if badge else ''
    footer_html = f'<div class="card-footer">{footer}</div>' if footer else ''
    
    return f"""
    <div class="card {card_class}" style="{card_style}">
        <h3 class="card-title">{title}</h3>
        <div class="card-content">{content}</div>
        {footer_html}
        {badge_html}
    </div>
    """

def render_card_decorative(title, content, footer=None, badge=None, card_class="", card_style=""):
    """Render a decorative card with title and content"""
    badge_html = f'<div class="badge badge-primary">{badge}</div>' if badge else ''
    footer_html = f'<div class="card-footer">{footer}</div>' if footer else ''
    
    return f"""
    <div class="card card-decorative {card_class}" style="{card_style}">
        <h3 class="card-title">{title}</h3>
        <div class="card-content">{content}</div>
        {footer_html}
        {badge_html}
    </div>
    """

def render_card_glass(title, content, footer=None, badge=None, card_class="", card_style=""):
    """Render a glass card with title and content"""
    badge_html = f'<div class="badge badge-primary">{badge}</div>' if badge else ''
    footer_html = f'<div class="card-footer">{footer}</div>' if footer else ''
    
    return f"""
    <div class="card card-glass {card_class}" style="{card_style}">
        <h3 class="card-title">{title}</h3>
        <div class="card-content">{content}</div>
        {footer_html}
        {badge_html}
    </div>
    """

def render_card_gradient(title, content, footer=None, badge=None, gradient="blue", card_class="", card_style=""):
    """Render a gradient card with title and content"""
    badge_html = f'<div class="badge badge-primary">{badge}</div>' if badge else ''
    footer_html = f'<div class="card-footer">{footer}</div>' if footer else ''
    
    return f"""
    <div class="card card-gradient-{gradient} {card_class}" style="{card_style}">
        <h3 class="card-title">{title}</h3>
        <div class="card-content">{content}</div>
        {footer_html}
        {badge_html}
    </div>
    """

def render_card_glow(title, content, footer=None, badge=None, card_class="", card_style=""):
    """Render a card with glowing border effect"""
    badge_html = f'<div class="badge badge-primary">{badge}</div>' if badge else ''
    footer_html = f'<div class="card-footer">{footer}</div>' if footer else ''
    
    return f"""
    <div class="card card-glow {card_class}" style="{card_style}">
        <h3 class="card-title">{title}</h3>
        <div class="card-content">{content}</div>
        {footer_html}
        {badge_html}
    </div>
    """

def render_badge(text, type="primary", pill=False):
    """Render a badge"""
    pill_class = "badge-pill" if pill else ""
    return f'<span class="badge badge-{type} {pill_class}">{text}</span>'

def render_avatar(name, size="md", type="gradient-blue", status=None):
    """Render an avatar"""
    initials = get_initials(name)
    status_class = f"avatar-status avatar-status-{status}" if status else ""
    
    return f'<div class="avatar avatar-{size} avatar-{type} {status_class}">{initials}</div>'

def render_avatar_group(names, size="md", max_display=4):
    """Render an avatar group"""
    if len(names) > max_display:
        visible_names = names[:max_display-1]
        more_count = len(names) - (max_display-1)
    else:
        visible_names = names
        more_count = 0
    
    avatars_html = ""
    for i, name in enumerate(visible_names):
        avatars_html += f'<div class="avatar avatar-{size} avatar-gradient-blue" style="transform: translateX(-{i*10}px);">{get_initials(name)}</div>'
    
    if more_count > 0:
        avatars_html += f'<div class="avatar avatar-{size}" style="transform: translateX(-{len(visible_names)*10}px); background: var(--color-neutral-500);">+{more_count}</div>'
    
    return f'<div class="avatar-group">{avatars_html}</div>'

def render_activity_item(user, action, time, icon=None, description=None):
    """Render an activity item"""
    icon_html = f'<div class="activity-icon">{icon}</div>' if icon else ''
    description_html = f'<div class="activity-description">{description}</div>' if description else ''
    
    return f"""
    <div class="activity-item animate-fade-in">
        {icon_html}
        <div class="activity-content">
            <div class="activity-header">
                <div class="activity-user">{user}</div>
                <div class="activity-time">{time}</div>
            </div>
            <div class="activity-description">{action}</div>
            {description_html}
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
        "event_reminder": "var(--color-primary-100)",
        "event": "var(--color-primary-100)",
        "promotion": "var(--color-tertiary-100)",
        "circle": "var(--color-secondary-100)",
        "login": "var(--color-success-100)",
        "media": "var(--color-primary-100)",
        "like": "var(--color-tertiary-100)",
        "comment": "var(--color-primary-100)",
        "follow": "var(--color-secondary-100)",
        "mention": "var(--color-primary-100)",
    }.get(notification_type, "var(--color-neutral-100)")
    
    text_color = {
        "event_reminder": "var(--color-primary-600)",
        "event": "var(--color-primary-600)",
        "promotion": "var(--color-tertiary-600)",
        "circle": "var(--color-secondary-600)",
        "login": "var(--color-success-600)",
        "media": "var(--color-primary-600)",
        "like": "var(--color-tertiary-600)",
        "comment": "var(--color-primary-600)",
        "follow": "var(--color-secondary-600)",
        "mention": "var(--color-primary-600)",
    }.get(notification_type, "var(--color-neutral-600)")
    
    # Format notification type for display
    display_type = notification_type.replace('_', ' ').title()
    
    return f"""
    <div class="notification-item {unread_class} animate-fade-in">
        <div class="notification-icon" style="background: {bg_color}; color: {text_color};">{icon}</div>
        <div class="notification-content">
            <div class="notification-header">
                <div class="notification-title">{display_type}</div>
                <div class="notification-time">{time_str}</div>
            </div>
            <div class="notification-body">{content}</div>
        </div>
    </div>
    """

def render_stat_card(value, label, icon=None, change=None, gradient=False):
    """Render a statistics card"""
    change_html = ""
    if change is not None:
        change_class = "stat-change-positive" if change >= 0 else "stat-change-negative"
        change_arrow = "↑" if change >= 0 else "↓"
        change_html = f"""
        <div class="{change_class}">
            {change_arrow} {abs(change)}%
        </div>
        """
    
    icon_class = "stat-icon-gradient" if gradient else ""
    icon_html = f'<div class="stat-icon {icon_class}">{icon}</div>' if icon else ''
    
    return f"""
    <div class="stat-card animate-fade-in">
        {icon_html}
        <div class="stat-content">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
            {change_html}
        </div>
    </div>
    """

def render_event_card(event, interactive=True, card_class=""):
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
        <div class="event-footer">
            <div class="event-location">
                📍 {event_location}
            </div>
            <div class="event-attendees">
                👥 {attendee_count} attending
            </div>
        </div>
        """
    
    return f"""
    <div class="event-card {card_class} animate-fade-in">
        <div class="event-image">
            <img src="{get_random_placeholder_image(image_seed)}" alt="{event_name}">
            <div class="event-date-badge">{formatted_date}</div>
        </div>
        <div class="event-content">
            <div class="event-meta">
                <div class="event-category">{event_circle}</div>
                <div class="event-time">🕒 {event_time}</div>
            </div>
            <h3 class="event-title">{event_name}</h3>
            <div class="event-description">{event_description[:100]}{'...' if len(event_description) > 100 else ''}</div>
            {buttons}
        </div>
    </div>
    """

def render_circle_card(circle, interactive=True, card_class=""):
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
        tags_html += f'<div class="badge badge-primary badge-pill">{tag}</div>'
    
    footer = ""
    if interactive:
        footer = f"""
        <div class="circle-footer">
            <div class="circle-privacy">
                {'🔒' if circle_type == 'private' else '🌐'} {circle_type.capitalize()}
            </div>
        </div>
        """
    
    # Generate gradient seed based on name
    gradient_seed = sum(ord(c) for c in circle_name) % 3
    gradient_class = ["gradient-blue", "gradient-purple", "gradient-pink"][gradient_seed]
    
    return f"""
    <div class="circle-card {card_class} animate-fade-in">
        <div class="circle-banner" style="background: var(--{gradient_class});"></div>
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
                {f'<div class="badge badge-neutral badge-pill">+{len(circle_tags) - 3} more</div>' if len(circle_tags) > 3 else ''}
            </div>
            
            {footer}
        </div>
    </div>
    """

def render_business_card(business, interactive=True, card_class=""):
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
    
    verified_badge = '<span class="business-verified-badge">✓</span>' if business_verified else ''
    
    return f"""
    <div class="business-card {card_class} animate-fade-in">
        <div class="business-header">
            <img src="{get_random_placeholder_image(logo_seed, 200, 200)}" class="business-logo" alt="{business_name}">
            <div class="business-info">
                <h3 class="business-name">
                    {business_name}
                    {verified_badge}
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
        </div>
    </div>
    """

def render_promotion_card(promotion, interactive=True, card_class=""):
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
    
    return f"""
    <div class="promotion-card {card_class} animate-fade-in">
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
    
    return f"""
    <div class="gallery-item animate-fade-in">
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
    
    verified_badge = '<span style="color: var(--color-primary-600); font-size: 0.9rem; margin-left: 4px;">✓</span>' if verified else ''
    
    return f"""
    <div class="profile-card animate-fade-in">
        <img src="data:image/png;base64,{avatar_data}" class="profile-avatar" style="width: 64px; height: 64px; border-radius: 50%; margin-right: 16px;">
        <div class="profile-info">
            <div class="profile-name">
                {full_name}
                {verified_badge}
            </div>
            <div class="profile-role" style="color: var(--color-primary-600);">{account_type.capitalize()}</div>
            <div class="profile-meta">
                <div>📍 {location}</div>
                <div>•</div>
                <div>Joined {joined_formatted}</div>
            </div>
        </div>
    </div>
    """

def render_timeline_item(title, date, content):
    """Render a timeline item"""
    return f"""
    <div class="timeline-item animate-fade-in">
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
    
    # Determine greeting based on time of day
    if 5 <= current_time.hour < 12:
        greeting = "Good morning"
        emoji = "🌅"
    elif 12 <= current_time.hour < 18:
        greeting = "Good afternoon"
        emoji = "☀️"
    else:
        greeting = "Good evening"
        emoji = "🌙"
    
    return f"""
    <div class="card card-gradient-blue animate-fade-in" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="color: white; margin-bottom: 8px; font-size: 1.75rem;">{greeting}, {name.split()[0]}! {emoji}</h2>
                <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 0;">Welcome back to your community. Discover what's happening today.</p>
            </div>
            <div style="font-size: 3rem; margin-left: 16px; transform: rotate(10deg);">👋</div>
        </div>
    </div>
    """

# ===== INITIALIZE DATABASES =====
init_db()
load_css()

# ===== AUTHENTICATION =====
def login():
    st.markdown("""
    <div class="welcome-container animate-fade-in">
        <div class="welcome-hero">
            <div class="welcome-content">
                <h1 class="welcome-title">Connect with your <span>community</span> like never before</h1>
                <p class="welcome-subtitle">Atmosphere brings people together based on shared interests, locations, and experiences. Discover communities, events, and businesses around you.</p>
                <div class="welcome-cta">
                    <button class="welcome-button welcome-button-primary">Get Started ➔</button>
                    <button class="welcome-button welcome-button-secondary">Learn More</button>
                </div>
            </div>
            <div class="welcome-image">
                <img src="https://images.unsplash.com/photo-1511632765486-a01980e01a18?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80" alt="Community">
            </div>
        </div>
        
        <div class="welcome-features">
            <div class="feature-card animate-fade-in animate-delay-100">
                <div class="feature-icon">👥</div>
                <h3 class="feature-title">Connect with Circles</h3>
                <p class="feature-description">Join communities based on your interests, hobbies, or location. Engage with like-minded people and build meaningful connections.</p>
            </div>
            <div class="feature-card animate-fade-in animate-delay-200">
                <div class="feature-icon">📅</div>
                <h3 class="feature-title">Discover Events</h3>
                <p class="feature-description">Find local events happening around you. From workshops to meetups, never miss out on experiences that matter to you.</p>
            </div>
            <div class="feature-card animate-fade-in animate-delay-300">
                <div class="feature-icon">🏬</div>
                <h3 class="feature-title">Support Local Businesses</h3>
                <p class="feature-description">Discover and support local businesses. Claim exclusive offers and promotions when you engage with their community.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown('<div class="auth-container animate-fade-in">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-header">
                <div class="auth-logo">🌍 Atmosphere</div>
                <div class="auth-subtitle">Sign in to your account</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("Email or Username", placeholder="Enter your email or username")
            st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.checkbox("Remember me")
            with col2:
                st.markdown('<div style="text-align: right;"><a href="#" class="auth-link">Forgot password?</a></div>', unsafe_allow_html=True)
            
            st.form_submit_button("Sign In", use_container_width=True)
        
        st.markdown("""
            <div class="auth-separator">OR</div>
            
            <button class="auth-button-social google">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                Continue with Google
            </button>
            
            <button class="auth-button-social facebook">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                Continue with Facebook
            </button>
            
            <button class="auth-button-social apple">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M16.462 8.583c-.307 0-1.085.312-1.924.312-.905 0-1.889-.321-1.889-.321s-.982.321-1.889.321c-.838 0-1.616-.312-1.924-.312C5.958 8.583 3 11.468 3 15.733c0 4.973 3.85 8.267 5.54 8.267.982 0 2.053-1.016 3.226-1.016 1.149 0 2.071 1.016 3.226 1.016 1.694 0 5.008-3.294 5.008-8.267 0-4.265-2.958-7.15-3.538-7.15zM14.35 5.265c1.317-1.599 1.209-3.147 1.184-3.265-1.205.071-2.495.886-3.205 1.866-.76.889-1.205 1.985-1.064 3.204 1.205.09 2.495-.72 3.085-1.805z"/></svg>
                Continue with Apple
            </button>
            
            <div class="auth-footer">
                Don't have an account? <a href="#" class="auth-link">Sign up</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def signup():
    st.markdown('<div class="auth-container animate-fade-in" style="max-width: 800px;">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="auth-header">
            <div class="auth-logo">🌍 Atmosphere</div>
            <div class="auth-subtitle">Create your account</div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Personal Account", "Business Account"])
    
    with tab1:
        with st.form("general_signup"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Full Name", placeholder="Enter your full name")
            with col2:
                st.text_input("Username", placeholder="Choose a username")
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Email", placeholder="Enter your email")
            with col2:
                st.text_input("Your Location", placeholder="City, Country")
                
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Password", type="password", placeholder="Create a password")
            with col2:
                st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
            st.multiselect("Your Interests", 
                          ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Fashion", "Books", "Movies"])
            
            st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.form_submit_button("Create Account", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True)
    
    with tab2:
        with st.form("business_signup"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Business Name", placeholder="Enter your business name")
            with col2:
                st.selectbox("Business Category", 
                          ["Food & Drink", "Retail", "Services", "Entertainment", "Health & Wellness", "Education", "Travel", "Other"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Owner/Representative Name", placeholder="Your full name")
            with col2:
                st.text_input("Username", placeholder="Choose a username")
                
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Business Email", placeholder="Enter business email")
            with col2:
                st.text_input("Business Address", placeholder="Full business address")
                
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Password", type="password", placeholder="Create a password")
            with col2:
                st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            st.text_area("Business Description", placeholder="Tell people about your business", height=100)
            
            st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.form_submit_button("Register Business", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True)
    
    st.markdown("""
        <div class="auth-separator">OR</div>
            
        <button class="auth-button-social google">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
            Continue with Google
        </button>
        
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
        <div class="card card-glass animate-fade-in" style="margin-bottom: 20px; border-left: 3px solid var(--color-primary-500);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div style="width: 48px; height: 48px; border-radius: 50%; background: var(--color-primary-100); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: var(--color-primary-600);">
                        🔔
                    </div>
                    <div>
                        <h3 style="margin-bottom: 4px;">You have {unread_count} unread notification{'s' if unread_count > 1 else ''}</h3>
                        <p style="margin: 0; color: var(--color-neutral-600);">Check your notifications to stay updated with your circles and events.</p>
                    </div>
                </div>
                <button class="welcome-button welcome-button-primary" style="padding: 8px 16px;">View Notifications</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # User stats
    st.markdown("## Your Activity")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_stat_card("5", "Circles Joined", "👥", change=10, gradient=True), unsafe_allow_html=True)
    with col2:
        st.markdown(render_stat_card("3", "Events Attended", "📅", change=0, gradient=True), unsafe_allow_html=True)
    with col3:
        st.markdown(render_stat_card("12", "Media Shared", "📸", change=20, gradient=True), unsafe_allow_html=True)
    with col4:
        st.markdown(render_stat_card("28", "Connections", "🔗", change=5, gradient=True), unsafe_allow_html=True)
    
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
            
            col1, col2 = st.columns([4, 1])
            with col2:
                st.button("Load More", use_container_width=True)
        
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
                        <div style="background: var(--color-neutral-50); border-radius: var(--radius-lg); padding: 16px; margin-bottom: 12px;">
                            <div style="font-weight: 600; margin-bottom: 6px;">{post['user']}</div>
                            <div style="margin-bottom: 8px;">{post['content']}</div>
                            <div style="color: var(--color-neutral-500); font-size: 0.8rem;">{post['time']}</div>
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
        st.markdown("""
        <h2 style="display: flex; align-items: center; gap: 8px;">
            <span>Upcoming Events</span>
            <span style="background: var(--color-primary-500); color: white; font-size: 0.75rem; padding: 2px 8px; border-radius: 20px;">3</span>
        </h2>
        """, unsafe_allow_html=True)
        
        # Sample events
        events = [
            {"name": "Sunset Photography", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
            {"name": "Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown", "circle": "Food Lovers", "description": "Explore various cuisines and dishes at the annual food festival."},
            {"name": "Tech Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Innovation Center", "circle": "Tech Enthusiasts", "description": "Network with tech professionals and learn about the latest innovations."}
        ]
        
        for i, event in enumerate(events):
            st.markdown(render_event_card(event, card_class=f"animate-fade-in animate-delay-{(i+1)*100}"), unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        with col2:
            st.button("View All Events", use_container_width=True)
    
    # Suggested circles
    st.markdown("## Suggested For You")
    
    col1, col2, col3 = st.columns(3)
    
    circles = [
        {"name": "NYC Photographers", "members": 245, "description": "For photography enthusiasts in NYC", "tags": ["Photography", "Art", "NYC"], "type": "public"},
        {"name": "Tech Innovators", "members": 189, "description": "Discuss the latest in technology", "tags": ["Technology", "Innovation", "Coding"], "type": "public"},
        {"name": "Foodies United", "members": 320, "description": "Discover and share great food spots", "tags": ["Food", "Restaurants", "Cooking"], "type": "public"}
    ]
    
    with col1:
        st.markdown(render_circle_card(circles[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
        st.button("Join Circle", key="join_1", use_container_width=True)
    
    with col2:
        st.markdown(render_circle_card(circles[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
        st.button("Join Circle", key="join_2", use_container_width=True)
    
    with col3:
        st.markdown(render_circle_card(circles[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
        st.button("Join Circle", key="join_3", use_container_width=True)
    
    if st.button("Discover More Circles", use_container_width=True):
        st.session_state["page"] = "circles"
        st.experimental_rerun()

def explore_page():
    # Header section with search
    st.markdown("""
    <div class="animate-fade-in" style="margin-bottom: 24px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 8px;">Explore</h1>
        <p style="color: var(--color-neutral-600); font-size: 1.1rem; margin-bottom: 24px;">Discover new circles, events, and people in your area</p>
        
        <div style="position: relative; margin-bottom: 24px;">
            <div style="position: absolute; top: 50%; transform: translateY(-50%); left: 16px; color: var(--color-neutral-500);">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            <input type="text" placeholder="Search for circles, events, or people..." style="width: 100%; padding: 16px 16px 16px 48px; border-radius: var(--radius-full); border: 1px solid var(--color-neutral-200); background: white; font-size: 1rem; box-shadow: var(--shadow-md);">
        </div>
        
        <div style="display: flex; gap: 12px; overflow-x: auto; padding: 8px 0; margin-bottom: 12px;">
            <div style="background: var(--color-primary-500); color: white; padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">All</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Circles</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Events</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">People</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Places</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Nearby</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Map view
    st.markdown("## 📍 Discover Around You")
    
    # Interactive map placeholder
    st.markdown("""
    <div class="card animate-fade-in" style="padding: 0; overflow: hidden; position: relative; min-height: 400px;">
        <div style="position: absolute; top: 16px; left: 16px; background: white; padding: 8px 16px; border-radius: var(--radius-lg); z-index: 10; box-shadow: var(--shadow-lg);">
            <span style="font-weight: 600; color: var(--color-neutral-900);">New York City</span>
        </div>
        
        <div style="position: absolute; top: 16px; right: 16px; display: flex; flex-direction: column; gap: 8px; z-index: 10;">
            <button style="width: 40px; height: 40px; border-radius: 50%; background: white; border: none; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-lg); cursor: pointer;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
            </button>
            <button style="width: 40px; height: 40px; border-radius: 50%; background: white; border: none; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-lg); cursor: pointer;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="8" y1="12" x2="16" y2="12"></line></svg>
            </button>
            <button style="width: 40px; height: 40px; border-radius: 50%; background: white; border: none; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-lg); cursor: pointer;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>
            </button>
        </div>
        
        <div style="position: absolute; bottom: 16px; right: 16px; background: white; padding: 8px; border-radius: var(--radius-lg); z-index: 10; box-shadow: var(--shadow-lg);">
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--color-primary-500);"></div>
                    <span style="font-size: 0.75rem; color: var(--color-neutral-700);">Circles (12)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--color-tertiary-500);"></div>
                    <span style="font-size: 0.75rem; color: var(--color-neutral-700);">Events (8)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--color-secondary-500);"></div>
                    <span style="font-size: 0.75rem; color: var(--color-neutral-700);">Places (5)</span>
                </div>
            </div>
        </div>
        
        <!-- Map image placeholder -->
        <img src="https://maps.googleapis.com/maps/api/staticmap?center=40.7128,-74.0060&zoom=12&size=1200x400&style=feature:water|color:0x4361ee&style=feature:road|color:0xffffff&style=element:labels|visibility:off&style=feature:poi|visibility:off&key=YOUR_API_KEY" style="width: 100%; height: 100%; object-fit: cover; object-position: center; aspect-ratio: 16/9;">
        
        <!-- Map markers -->
        <div style="position: absolute; top: 40%; left: 30%;">
            <div class="map-marker">
                <div class="map-marker-content">12</div>
            </div>
        </div>
        <div style="position: absolute; top: 60%; left: 50%;">
            <div class="map-marker" style="background: var(--color-tertiary-500);">
                <div class="map-marker-content">8</div>
            </div>
        </div>
        <div style="position: absolute; top: 30%; left: 70%;">
            <div class="map-marker" style="background: var(--color-secondary-500);">
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
            {"name": "NYC Photographers", "members": 245, "description": "For photography enthusiasts in NYC", "tags": ["Photography", "Art", "NYC"], "type": "public"},
            {"name": "Tech Innovators", "members": 189, "description": "Discuss the latest in technology", "tags": ["Technology", "Innovation", "Coding"], "type": "public"},
            {"name": "Foodies United", "members": 320, "description": "Discover and share great food spots", "tags": ["Food", "Restaurants", "Cooking"], "type": "public"},
            {"name": "Outdoor Adventures", "members": 156, "description": "Explore the great outdoors together", "tags": ["Nature", "Hiking", "Adventure"], "type": "public"},
            {"name": "Book Club NYC", "members": 112, "description": "Monthly book discussions and recommendations", "tags": ["Books", "Reading", "Literature"], "type": "private"},
            {"name": "Fitness Enthusiasts", "members": 278, "description": "Workouts, nutrition tips, and wellness", "tags": ["Fitness", "Health", "Wellness"], "type": "public"}
        ]
        
        with col1:
            st.markdown(render_circle_card(circles[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_c1", use_container_width=True)
            st.markdown(render_circle_card(circles[3], card_class="animate-fade-in animate-delay-400"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_c4", use_container_width=True)
        
        with col2:
            st.markdown(render_circle_card(circles[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_c2", use_container_width=True)
            st.markdown(render_circle_card(circles[4], card_class="animate-fade-in animate-delay-500"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_c5", use_container_width=True)
        
        with col3:
            st.markdown(render_circle_card(circles[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_c3", use_container_width=True)
            st.markdown(render_circle_card(circles[5], card_class="animate-fade-in animate-delay-600"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_c6", use_container_width=True)
    
    with tab2:
        st.markdown("### Upcoming Events")
        col1, col2 = st.columns(2)
        
        events = [
            {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
            {"name": "International Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown City Park", "circle": "Food Lovers", "description": "Explore various cuisines and dishes at the annual food festival."},
            {"name": "Tech Innovation Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Tech Innovation Center", "circle": "Tech Enthusiasts", "description": "Network with tech professionals and learn about the latest innovations."},
            {"name": "Morning Yoga in the Park", "date": "Jun 18", "time": "8:00 AM", "location": "Central Park", "circle": "Fitness Community", "description": "Start your day with energizing yoga in the park."}
        ]
        
        with col1:
            st.markdown(render_event_card(events[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
            st.button("RSVP", key="rsvp_1", use_container_width=True)
            st.markdown(render_event_card(events[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
            st.button("RSVP", key="rsvp_3", use_container_width=True)
        
        with col2:
            st.markdown(render_event_card(events[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
            st.button("RSVP", key="rsvp_2", use_container_width=True)
            st.markdown(render_event_card(events[3], card_class="animate-fade-in animate-delay-400"), unsafe_allow_html=True)
            st.button("RSVP", key="rsvp_4", use_container_width=True)
    
    with tab3:
        st.markdown("### Popular Places")
        col1, col2, col3 = st.columns(3)
        
        businesses = [
            {"business_name": "Artisan Cafe", "category": "Coffee & Bakery", "locations": [{"address": "123 Main St, New York"}], "verified": True, "description": "Cozy cafe with specialty coffee, pastries, and a relaxed atmosphere perfect for working or socializing."},
            {"business_name": "Innovation Hub", "category": "Co-Working Space", "locations": [{"address": "456 Tech Ave, New York"}], "verified": True, "description": "Modern co-working space with high-speed internet, meeting rooms, and a vibrant community of professionals."},
            {"business_name": "Green Table Restaurant", "category": "Farm-to-Table Dining", "locations": [{"address": "789 Park Rd, New York"}], "verified": False, "description": "Farm-to-table restaurant serving seasonal, locally-sourced ingredients with an emphasis on sustainability."}
        ]
        
        with col1:
            st.markdown(render_business_card(businesses[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
            st.button("Follow", key="follow_b1", use_container_width=True)
        
        with col2:
            st.markdown(render_business_card(businesses[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
            st.button("Follow", key="follow_b2", use_container_width=True)
        
        with col3:
            st.markdown(render_business_card(businesses[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
            st.button("Follow", key="follow_b3", use_container_width=True)
    
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
            st.button("Connect", key="connect_1", use_container_width=True)
        
        with col2:
            st.markdown(render_profile_card(users[1]), unsafe_allow_html=True)
            st.button("Connect", key="connect_2", use_container_width=True)
        
        with col3:
            st.markdown(render_profile_card(users[2]), unsafe_allow_html=True)
            st.button("Connect", key="connect_3", use_container_width=True)
        
        with col4:
            st.markdown(render_profile_card(users[3]), unsafe_allow_html=True)
            st.button("Connect", key="connect_4", use_container_width=True)
    
    # Popular hashtags
    st.markdown("### 🔖 Trending Topics")
    
    st.markdown("""
    <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px;" class="animate-fade-in">
        <div style="background: var(--gradient-blue); color: white; padding: 12px 20px; border-radius: var(--radius-full); font-weight: 500; box-shadow: var(--shadow-md); transition: var(--transition-all); cursor: pointer;">
            #Photography <span style="opacity: 0.8; margin-left: 4px; font-size: 0.875rem;">1.2K</span>
        </div>
        <div style="background: var(--gradient-purple); color: white; padding: 12px 20px; border-radius: var(--radius-full); font-weight: 500; box-shadow: var(--shadow-md); transition: var(--transition-all); cursor: pointer;">
            #FoodFestNYC <span style="opacity: 0.8; margin-left: 4px; font-size: 0.875rem;">895</span>
        </div>
        <div style="background: var(--gradient-pink); color: white; padding: 12px 20px; border-radius: var(--radius-full); font-weight: 500; box-shadow: var(--shadow-md); transition: var(--transition-all); cursor: pointer;">
            #TechTalks <span style="opacity: 0.8; margin-left: 4px; font-size: 0.875rem;">752</span>
        </div>
        <div style="background: var(--gradient-blue); color: white; padding: 12px 20px; border-radius: var(--radius-full); font-weight: 500; box-shadow: var(--shadow-md); transition: var(--transition-all); cursor: pointer;">
            #SummerInTheCity <span style="opacity: 0.8; margin-left: 4px; font-size: 0.875rem;">634</span>
        </div>
        <div style="background: var(--gradient-purple); color: white; padding: 12px 20px; border-radius: var(--radius-full); font-weight: 500; box-shadow: var(--shadow-md); transition: var(--transition-all); cursor: pointer;">
            #CentralParkEvents <span style="opacity: 0.8; margin-left: 4px; font-size: 0.875rem;">521</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Featured promotions
    st.markdown("## Special Offers")
    col1, col2, col3 = st.columns(3)
    
    promotions = [
        {"name": "Summer Special", "offer": "20% off all items", "description": "Enjoy summer savings on all menu items at Artisan Cafe. Limited time only!", "requirements": "Show this offer to the cashier when ordering.", "start_date": "2023-06-01", "end_date": "2023-08-31", "claimed_by": ["usr_1", "usr_2", "usr_3"]},
        {"name": "Photo Contest", "offer": "Win a free camera", "description": "Submit your best photos for a chance to win a professional camera from Photography Pro Shop.", "requirements": "Post 3 photos with #PhotoContest and tag our business.", "start_date": "2023-06-15", "end_date": "2023-07-15", "claimed_by": ["usr_1"]},
        {"name": "First-Time Customer", "offer": "Free dessert", "description": "New customers get a free dessert with any meal purchase at Green Table Restaurant.", "requirements": "Mention this offer when ordering. First-time customers only.", "start_date": "2023-06-01", "end_date": "2023-12-31", "claimed_by": ["usr_1", "usr_2"]}
    ]
    
    with col1:
        st.markdown(render_promotion_card(promotions[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
        st.button("Claim Offer", key="claim_1", use_container_width=True)
    
    with col2:
        st.markdown(render_promotion_card(promotions[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
        st.button("Claim Offer", key="claim_2", use_container_width=True)
    
    with col3:
        st.markdown(render_promotion_card(promotions[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
        st.button("Claim Offer", key="claim_3", use_container_width=True)

def media_page():
    # Header with title and tabs
    st.markdown("""
    <div class="animate-fade-in" style="margin-bottom: 24px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 8px;">Media Gallery</h1>
        <p style="color: var(--color-neutral-600); font-size: 1.1rem; margin-bottom: 24px;">Capture, share, and discover moments with your community</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        
        col1, col2 = st.columns([3, 1])
        with col2:
            st.button("Load More", use_container_width=True)
    
    with tab2:
        st.markdown("### Share Your Moments")
        
        # Upload options with modern styling
        st.markdown("""
        <div class="card card-decorative animate-fade-in" style="margin-bottom: 24px; padding: 32px; text-align: center;">
            <div style="max-width: 500px; margin: 0 auto;">
                <div style="font-size: 4rem; margin-bottom: 16px;">📸</div>
                <h3 style="margin-bottom: 16px; font-size: 1.5rem;">Upload a Photo or Video</h3>
                <p style="color: var(--color-neutral-600); margin-bottom: 24px;">Share your moments with your circles and the Atmosphere community.</p>
                <div style="display: flex; gap: 16px; justify-content: center;">
                    <button class="welcome-button welcome-button-primary" style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                        Take Photo
                    </button>
                    <button class="welcome-button welcome-button-secondary" style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                        Upload File
                    </button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Camera capture with stylish container
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
            <div style="background: var(--gradient-blue); color: white; padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">All</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Nature</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Urban</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">People</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Food</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Art</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Technology</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Travel</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Masonry gallery layout
        st.markdown("""
        <div style="columns: 4 200px; column-gap: 16px;" class="animate-fade-in">
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682685797898-6d7587974771?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@photoEnthusiast</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>2h ago</div>
                        <div>❤️ 24</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682687220063-4742bd7fd538?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@travelLover</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>5h ago</div>
                        <div>❤️ 38</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682686581776-b62f563de74f?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@naturePics</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>1d ago</div>
                        <div>❤️ 92</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682687220067-dced9a881b56?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@foodieCritic</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>2d ago</div>
                        <div>❤️ 56</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682687220123-2a3473130a9d?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@cityViews</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>3d ago</div>
                        <div>❤️ 77</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682685797828-d3b2561deef4?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@artGallery</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>4d ago</div>
                        <div>❤️ 41</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682686580391-8b2263139d7a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@urbanLife</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>5d ago</div>
                        <div>❤️ 63</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1682685797365-41f45b562c0a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; margin-bottom: 4px;">@winterWanderer</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; opacity: 0.8;">
                        <div>1w ago</div>
                        <div>❤️ 88</div>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            /* Add hover effects for gallery */
            div[style*="break-inside: avoid"]:hover img {
                transform: scale(1.05);
                transition: transform 0.5s ease;
            }
            
            div[style*="break-inside: avoid"]:hover div[style*="position: absolute"] {
                opacity: 1;
                transform: translateY(0);
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            st.button("Explore More", use_container_width=True)

def circles_page():
    # Header with title and features
    st.markdown("""
    <div class="animate-fade-in" style="margin-bottom: 24px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 8px;">Circles</h1>
        <p style="color: var(--color-neutral-600); font-size: 1.1rem; margin-bottom: 24px;">Connect with communities based on shared interests and experiences</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(render_circle_card(user_circles[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
            st.button("View Circle", key="view_c1", use_container_width=True)
        
        with col2:
            st.markdown(render_circle_card(user_circles[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
            st.button("View Circle", key="view_c2", use_container_width=True)
        
        with col3:
            st.markdown(render_circle_card(user_circles[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
            st.button("View Circle", key="view_c3", use_container_width=True)
        
        st.markdown("### Circle Activity")
        
        # Display activities for the first circle (as an example)
        if user_circles:
            circle = user_circles[0]
            st.markdown(f"#### Recent in {circle['name']}")
            
            st.markdown('<div class="timeline animate-fade-in">', unsafe_allow_html=True)
            
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
            st.markdown("""
            <div style="position: relative; margin-bottom: 24px;">
                <div style="position: absolute; top: 50%; transform: translateY(-50%); left: 16px; color: var(--color-neutral-500);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                </div>
                <input type="text" placeholder="Search circles by name, interest, or location..." style="width: 100%; padding: 16px 16px 16px 48px; border-radius: var(--radius-full); border: 1px solid var(--color-neutral-200); background: white; font-size: 1rem; box-shadow: var(--shadow-md);">
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.selectbox("Sort by", ["Popular", "New", "Active", "Nearby"])
        
        # Categories quick filter
        st.markdown("""
        <div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px 0; margin-bottom: 20px;">
            <div style="background: var(--color-primary-500); color: white; padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">All Categories</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Photography</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Food</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Technology</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Sports</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Art</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-800); padding: 8px 16px; border-radius: var(--radius-full); white-space: nowrap;">Music</div>
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
            st.markdown(render_circle_card(circles[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_discover_1", use_container_width=True)
            st.markdown(render_circle_card(circles[3], card_class="animate-fade-in animate-delay-400"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_discover_4", use_container_width=True)
        
        with col2:
            st.markdown(render_circle_card(circles[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_discover_2", use_container_width=True)
            st.markdown(render_circle_card(circles[4], card_class="animate-fade-in animate-delay-500"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_discover_5", use_container_width=True)
        
        with col3:
            st.markdown(render_circle_card(circles[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_discover_3", use_container_width=True)
            st.markdown(render_circle_card(circles[5], card_class="animate-fade-in animate-delay-600"), unsafe_allow_html=True)
            st.button("Join Circle", key="join_discover_6", use_container_width=True)
        
        col1, col2 = st.columns([4, 1])
        with col2:
            st.button("Load More", use_container_width=True)
    
    with tab3:
        st.markdown("### Create a New Circle")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("create_circle"):
                # Circle details
                st.markdown("#### Basic Information")
                st.text_input("Circle Name", placeholder="Give your circle a catchy name")
                st.text_area("Description", placeholder="What's your circle about?", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.radio("Privacy Type", ["Public", "Private"])
                with col2:
                    st.text_input("Primary Location", placeholder="City, Country (optional)")
                
                # Additional settings
                st.markdown("#### Circle Settings")
                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox("Require approval for new members")
                with col2:
                    st.checkbox("Require approval for posts")
                
                # Tags
                st.multiselect("Tags (helps people find your circle)", 
                            ["Art", "Music", "Sports", "Food", "Tech", "Nature", "Travel", "Photography", "Books", "Movies", "Fashion", "Education"])
                
                # Cover image
                st.markdown("#### Circle Image")
                st.file_uploader("Upload a cover image (optional)", type=["jpg", "jpeg", "png"])
                
                # Submit
                col1, col2 = st.columns(2)
                with col1:
                    st.form_submit_button("Create Circle", use_container_width=True)
                with col2:
                    st.form_submit_button("Cancel", use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="card card-gradient-blue" style="color: white;">
                <h3 class="card-title" style="color: white;">Circle Guidelines</h3>
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
            
            <div class="card card-glass" style="margin-top: 24px;">
                <h3 class="card-title">Circle Analytics</h3>
                <div class="card-content">
                    <p>Once your circle is created, you'll get access to member engagement statistics, popular content insights, and growth metrics.</p>
                    <div style="margin-top: 16px;">
                        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" style="width: 100%; border-radius: var(--radius-lg);">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def events_page():
    # Header with title and description
    st.markdown("""
    <div class="animate-fade-in" style="margin-bottom: 24px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 8px;">Events</h1>
        <p style="color: var(--color-neutral-600); font-size: 1.1rem; margin-bottom: 24px;">Discover and create exciting events in your community</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Discover Events", "Your Events", "Create Event"])
    
    with tab1:
        st.markdown("### Find Events Near You")
        
        # Filters with modern styling
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
        <div class="card card-glass" style="padding: 0; overflow: hidden; position: relative; margin-bottom: 24px;">
            <img src="https://images.unsplash.com/photo-1540575467063-178a50c2df87?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" style="width: 100%; height: 300px; object-fit: cover;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0.2), transparent); display: flex; flex-direction: column; justify-content: flex-end; padding: 32px;">
                <div style="background: var(--color-primary-500); color: white; display: inline-block; padding: 4px 12px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600; margin-bottom: 12px; width: fit-content;">FEATURED EVENT</div>
                <h2 style="color: white; margin-bottom: 12px; font-size: 2.5rem;">NYC Summer Photography Festival</h2>
                <div style="color: rgba(255,255,255,0.9); display: flex; flex-wrap: wrap; gap: 24px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                        June 24-26, 2023
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                        Central Park, New York
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                        243 attending
                    </div>
                </div>
                <button class="welcome-button welcome-button-primary" style="width: fit-content;">View Details</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if view_type == "Calendar":
            # Calendar view
            st.markdown("""
            <div class="card animate-fade-in" style="margin-bottom: 24px;">
                <h3 class="card-title">June 2023</h3>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: 600; margin-bottom: 16px; border-bottom: 1px solid var(--color-neutral-200); padding-bottom: 8px;">
                    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(7, 1fr); grid-gap: 8px;">
                    <div style="padding: 12px; text-align: center; color: var(--color-neutral-400);">28</div>
                    <div style="padding: 12px; text-align: center; color: var(--color-neutral-400);">29</div>
                    <div style="padding: 12px; text-align: center; color: var(--color-neutral-400);">30</div>
                    <div style="padding: 12px; text-align: center; color: var(--color-neutral-400);">31</div>
                    <div style="padding: 12px; text-align: center;">1</div>
                    <div style="padding: 12px; text-align: center;">2</div>
                    <div style="padding: 12px; text-align: center;">3</div>
                    
                    <div style="padding: 12px; text-align: center;">4</div>
                    <div style="padding: 12px; text-align: center;">5</div>
                    <div style="padding: 12px; text-align: center;">6</div>
                    <div style="padding: 12px; text-align: center;">7</div>
                    <div style="padding: 12px; text-align: center;">8</div>
                    <div style="padding: 12px; text-align: center;">9</div>
                    <div style="padding: 12px; text-align: center;">10</div>
                    
                    <div style="padding: 12px; text-align: center;">11</div>
                    <div style="padding: 12px; text-align: center;">12</div>
                    <div style="padding: 12px; text-align: center;">13</div>
                    <div style="padding: 12px; text-align: center;">14</div>
                    <div style="padding: 12px; text-align: center; background: rgba(59, 130, 246, 0.1); border-radius: var(--radius-lg); border: 2px solid var(--color-primary-500); color: var(--color-primary-700); font-weight: bold; position: relative;">
                        15
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-primary-500); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 12px; text-align: center; position: relative;">
                        16
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-primary-500); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 12px; text-align: center;">17</div>
                    
                    <div style="padding: 12px; text-align: center; position: relative;">
                        18
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-secondary-500); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 12px; text-align: center;">19</div>
                    <div style="padding: 12px; text-align: center; position: relative;">
                        20
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-tertiary-500); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 12px; text-align: center;">21</div>
                    <div style="padding: 12px; text-align: center;">22</div>
                    <div style="padding: 12px; text-align: center;">23</div>
                    <div style="padding: 12px; text-align: center; position: relative; background: rgba(128, 91, 224, 0.1); border-radius: var(--radius-lg);">
                        24
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-secondary-500); border-radius: 50%;"></div>
                    </div>
                    
                    <div style="padding: 12px; text-align: center; position: relative; background: rgba(128, 91, 224, 0.1); border-radius: var(--radius-lg);">
                        25
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-secondary-500); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 12px; text-align: center; position: relative; background: rgba(128, 91, 224, 0.1); border-radius: var(--radius-lg);">
                        26
                        <div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: var(--color-secondary-500); border-radius: 50%;"></div>
                    </div>
                    <div style="padding: 12px; text-align: center;">27</div>
                    <div style="padding: 12px; text-align: center;">28</div>
                    <div style="padding: 12px; text-align: center;">29</div>
                    <div style="padding: 12px; text-align: center;">30</div>
                    <div style="padding: 12px; text-align: center; color: var(--color-neutral-400);">1</div>
                </div>
                <div style="margin-top: 20px; display: flex; gap: 24px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--color-primary-500);"></div>
                        <div>Your events</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--color-secondary-500);"></div>
                        <div>Photography Festival</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--color-tertiary-500);"></div>
                        <div>Popular events</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Calendar day details
            st.markdown("### Events on June 15")
            
            # Use the event card component for events on this day
            event = {
                "name": "Sunset Photography Workshop", 
                "date": "Jun 15", 
                "time": "6:00 PM", 
                "location": "Brooklyn Bridge", 
                "circle": "NYC Photographers",
                "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge. Learn techniques for capturing stunning sunset images with professional photographers."
            }
            
            st.markdown(render_event_card(event, card_class="animate-fade-in"), unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.button("RSVP", key="rsvp_cal_1", use_container_width=True)
            with col2:
                st.button("Add to Calendar", key="cal_add_1", use_container_width=True)
            
        else:
            # List view
            st.markdown("### Upcoming Events")
            
            # Grid layout for events
            col1, col2 = st.columns(2)
            
            # Sample events
            events = [
                {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "location": "Brooklyn Bridge", "circle": "NYC Photographers", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
                {"name": "International Food Festival", "date": "Jun 20", "time": "12:00 PM", "location": "Downtown City Park", "circle": "Food Lovers", "description": "Explore various cuisines and dishes at the annual food festival."},
                {"name": "Tech Innovation Meetup", "date": "Jul 2", "time": "7:00 PM", "location": "Tech Innovation Center", "circle": "Tech Enthusiasts", "description": "Network with tech professionals and learn about the latest innovations."},
                {"name": "Morning Yoga in the Park", "date": "Jun 18", "time": "8:00 AM", "location": "Central Park", "circle": "Fitness Community", "description": "Start your day with energizing yoga in the park."}
            ]
            
            with col1:
                st.markdown(render_event_card(events[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.button("RSVP", key="rsvp_list_1", use_container_width=True)
                with col2:
                    st.button("Details", key="details_1", use_container_width=True)
                
                st.markdown(render_event_card(events[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.button("RSVP", key="rsvp_list_3", use_container_width=True)
                with col2:
                    st.button("Details", key="details_3", use_container_width=True)
            
            with col2:
                st.markdown(render_event_card(events[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.button("RSVP", key="rsvp_list_2", use_container_width=True)
                with col2:
                    st.button("Details", key="details_2", use_container_width=True)
                
                st.markdown(render_event_card(events[3], card_class="animate-fade-in animate-delay-400"), unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.button("RSVP", key="rsvp_list_4", use_container_width=True)
                with col2:
                    st.button("Details", key="details_4", use_container_width=True)
            
            col1, col2 = st.columns([4, 1])
            with col2:
                st.button("View More", use_container_width=True)
    
    with tab2:
        st.markdown("### Your Events")
        
        # Event categories with pills
        st.markdown("""
        <div style="display: flex; gap: 8px; margin-bottom: 24px;">
            <div style="background: var(--color-primary-500); color: white; padding: 8px 16px; border-radius: var(--radius-full); font-weight: 500; cursor: pointer;">Attending</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-700); padding: 8px 16px; border-radius: var(--radius-full); font-weight: 500; cursor: pointer;">Organized</div>
            <div style="background: var(--color-neutral-100); color: var(--color-neutral-700); padding: 8px 16px; border-radius: var(--radius-full); font-weight: 500; cursor: pointer;">Past Events</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display attending events
        # Sample user events
        user_events = [
            {"name": "Sunset Photography Workshop", "date": "Jun 15", "time": "6:00 PM", "status": "Confirmed", "role": "Attendee", "description": "Join us for a beautiful sunset photography session at the iconic Brooklyn Bridge."},
            {"name": "Tech Book Club", "date": "Jun 22", "time": "7:00 PM", "status": "Pending", "role": "Attendee", "description": "Discussion of 'The Innovators' by Walter Isaacson."}
        ]
        
        if not user_events:
            st.info("You're not attending any upcoming events yet. Explore events to join!")
        else:
            for i, event in enumerate(user_events):
                status_color = "var(--color-primary-500)" if event['status'] == 'Confirmed' else "var(--color-warning-500)"
                status_bg = "rgba(59, 130, 246, 0.1)" if event['status'] == 'Confirmed' else "rgba(245, 158, 11, 0.1)"
                
                st.markdown(f"""
                <div class="card animate-fade-in animate-delay-{(i+1)*100}" style="margin-bottom: 20px; {'' if event['status'] == 'Confirmed' else 'border-left: 3px solid var(--color-warning-500);'}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <h3 style="margin: 0;">{event['name']}</h3>
                        <div style="background: {status_bg}; color: {status_color}; padding: 4px 12px; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500;">{event['status']}</div>
                    </div>
                    <div style="margin-bottom: 16px;">
                        <div style="display: flex; flex-wrap: wrap; gap: 16px; color: var(--color-neutral-700);">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                                {event['date']} at {event['time']}
                            </div>
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                                {event['role']}
                            </div>
                        </div>
                    </div>
                    <p>{event['description']}</p>
                    <div style="display: flex; gap: 12px; margin-top: 16px;">
                        <button class="welcome-button welcome-button-primary" style="flex: 1;">View Details</button>
                        {'<button class="welcome-button welcome-button-secondary" style="flex: 1;">Cancel RSVP</button>' if event['status'] == 'Confirmed' else '<button class="welcome-button welcome-button-primary" style="flex: 1;">Confirm</button>'}
                        <button class="welcome-button welcome-button-secondary" style="width: auto; padding: 8px; aspect-ratio: 1;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                        </button>
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
                st.text_input("Event Name", placeholder="Give your event a clear, descriptive name")
                st.text_area("Description", placeholder="What's your event about? Include all important details.", height=100)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.date_input("Date")
                with col2:
                    st.time_input("Time")
                
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
                st.markdown("#### Event Cover Image")
                cover_image = st.file_uploader("Upload a cover image (optional)", type=["jpg", "jpeg", "png"])
                
                # Submit
                col1, col2 = st.columns(2)
                with col1:
                    st.form_submit_button("Create Event", use_container_width=True)
                with col2:
                    st.form_submit_button("Cancel", use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="card card-gradient-purple" style="color: white;">
                <h3 class="card-title" style="color: white;">Event Creation Tips</h3>
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
            
            <div class="card card-glass" style="margin-top: 24px;">
                <h3 class="card-title">Location Tips</h3>
                <div class="card-content">
                    <p>For in-person events, choose locations that are:</p>
                    <ul>
                        <li>Easy to find and access</li>
                        <li>Suitable for your planned activities</li>
                        <li>Have adequate capacity for expected attendees</li>
                        <li>Offer necessary amenities (parking, restrooms, etc.)</li>
                    </ul>
                    <p>For online events, provide clear instructions for accessing the virtual meeting room.</p>
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
    
    # Business overview header with premium styling
    business_info = st.session_state.get("business", {})
    business_name = business_info.get("business_name", "Your Business")
    business_category = business_info.get("category", "")
    
    st.markdown(f"""
    <div class="card card-gradient-blue animate-fade-in" style="color: white; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h1 style="color: white; margin-bottom: 8px; font-size: 2.5rem;">{business_name}</h1>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px;">
                    <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: var(--radius-full); font-size: 0.875rem;">{business_category}</span>
                    {render_badge("Premium", "primary", True) if business_info.get("verified", False) else render_badge("Unverified", "neutral", True)}
                </div>
                <div style="display: flex; gap: 32px; margin-top: 24px;">
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 700;">245</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Followers</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 700;">56</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Mentions</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 700;">3</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Promos</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 700;">82%</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Rating</div>
                    </div>
                </div>
            </div>
            <div>
                <button class="welcome-button welcome-button-secondary" style="background: rgba(255,255,255,0.2); border: none; color: white;">Edit Profile</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Promotions", "Analytics", "Settings"])
    
    with tab1:
        # Quick actions row with modern buttons
        st.markdown("### Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <button class="welcome-button welcome-button-primary" style="width: 100%; justify-content: center; gap: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                Create Promotion
            </button>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <button class="welcome-button welcome-button-primary" style="width: 100%; justify-content: center; gap: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                Post Update
            </button>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <button class="welcome-button welcome-button-primary" style="width: 100%; justify-content: center; gap: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                Create Event
            </button>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <button class="welcome-button welcome-button-primary" style="width: 100%; justify-content: center; gap: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                Contact Followers
            </button>
            """, unsafe_allow_html=True)
        
        # Activity and engagement in a modern layout
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
            
            col1, col2 = st.columns([4, 1])
            with col2:
                st.button("View All", use_container_width=True)
        
        with col2:
            st.markdown("### Engagement Summary")
            
            # Engagement metrics with modern styling
            st.markdown("""
            <div class="card animate-fade-in">
                <h3 class="card-title">Last 7 Days</h3>
                
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <div>Profile Views</div>
                        <div style="font-weight: 600;">127</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 75%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <div>Media Tags</div>
                        <div style="font-weight: 600;">23</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 40%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <div>New Followers</div>
                        <div style="font-weight: 600;">18</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 30%;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <div>Promotion Claims</div>
                        <div style="font-weight: 600;">12</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 25%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Business Circle
        st.markdown("### Your Business Circle")
        if not business_info.get("has_circle", False):
            st.markdown("""
            <div class="card card-glass animate-fade-in">
                <div style="display: flex; gap: 24px; align-items: center;">
                    <div style="font-size: 3rem;">👥</div>
                    <div style="flex-grow: 1;">
                        <h3 style="margin-bottom: 8px;">Create Your Business Circle</h3>
                        <p style="margin-bottom: 16px;">Connect directly with your customers by creating a dedicated circle for your business. Share updates, promotions, and events with your community.</p>
                        <button class="welcome-button welcome-button-primary">Create Business Circle</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("Your business circle has 86 members")
            st.button("Manage Circle", use_container_width=True)

            # Media mentions with masonry gallery
        st.markdown("### Media Mentions")
        st.markdown("<p>Recent photos and posts that mention your business</p>", unsafe_allow_html=True)
        
        # Grid of media with modern styling
        st.markdown("""
        <div style="columns: 6 120px; column-gap: 16px; margin-bottom: 24px;" class="animate-fade-in">
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cmVzdGF1cmFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; font-size: 0.75rem;">@user1</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; opacity: 0.8;">
                        <div>2h ago</div>
                        <div>❤️ 24</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1578474846511-04ba529f0b88?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Y2FmZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; font-size: 0.75rem;">@user2</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; opacity: 0.8;">
                        <div>5h ago</div>
                        <div>❤️ 18</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cmVzdGF1cmFudCUyMGludGVyaW9yfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; font-size: 0.75rem;">@foodieLover</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; opacity: 0.8;">
                        <div>1d ago</div>
                        <div>❤️ 42</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8Zm9vZHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; font-size: 0.75rem;">@cuisine_hunter</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; opacity: 0.8;">
                        <div>2d ago</div>
                        <div>❤️ 37</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1484980972926-edee96e0960d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjB8fGZvb2R8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; font-size: 0.75rem;">@plate_perfect</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; opacity: 0.8;">
                        <div>3d ago</div>
                        <div>❤️ 29</div>
                    </div>
                </div>
            </div>
            <div style="break-inside: avoid; margin-bottom: 16px; position: relative; border-radius: var(--radius-lg); overflow: hidden; transition: all 0.3s ease;">
                <img src="https://images.unsplash.com/photo-1513442542250-854d436a73f2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8c3RyZWV0JTIwZm9vZHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; border-radius: var(--radius-lg); display: block;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 8px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; opacity: 0; transform: translateY(10px); transition: all 0.3s ease;">
                    <div style="font-weight: 600; font-size: 0.75rem;">@street_eats</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.6rem; opacity: 0.8;">
                        <div>4d ago</div>
                        <div>❤️ 53</div>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            /* Add hover effects for gallery */
            div[style*="break-inside: avoid"]:hover img {
                transform: scale(1.05);
                transition: transform 0.5s ease;
            }
            
            div[style*="break-inside: avoid"]:hover div[style*="position: absolute"] {
                opacity: 1;
                transform: translateY(0);
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col2:
            st.button("View All Mentions", key="view_mentions", use_container_width=True)
    
    with tab2:
        st.markdown("### Manage Promotions")
        
        # Create promotion form
        st.markdown("""
        <div class="card card-glass animate-fade-in">
            <h3 class="card-title">Create New Promotion</h3>
            <p style="margin-bottom: 24px; color: var(--color-neutral-600);">Design an offer that drives engagement and brings customers to your business.</p>
        """, unsafe_allow_html=True)
        
        with st.form("create_promotion"):
            col1, col2 = st.columns(2)
            
            with col1:
                promo_name = st.text_input("Promotion Name", placeholder="E.g., Summer Special, Happy Hour Deal")
                promo_offer = st.text_input("Offer Details", placeholder="E.g., 20% off, Free dessert, Buy one get one free")
                
                st.markdown("#### Valid Period")
                col1a, col1b = st.columns(2)
                with col1a:
                    start_date = st.date_input("Start Date", value=datetime.now())
                with col1b:
                    end_date = st.date_input("End Date", value=datetime.now() + timedelta(days=30))
            
            with col2:
                promo_desc = st.text_area("Description", height=100, placeholder="Describe your promotion in detail...")
                promo_req = st.text_area("Requirements", height=100, placeholder="What users need to do to claim this offer (e.g., Post 3 photos, Check-in at location)")
                
                promo_limit = st.number_input("Redemption Limit (0 for unlimited)", min_value=0, value=50)
                
            # Targeting options
            st.markdown("#### Targeting")
            col1, col2 = st.columns(2)
            with col1:
                target_circles = st.multiselect("Available to Circles", 
                                            ["All Circles", "NYC Photographers", "Food Lovers", "Tech Enthusiasts"])
            with col2:
                required_tags = st.text_input("Required Hashtags", placeholder="E.g., #YourBusiness #SpecialOffer (comma separated)")
                
            # Promotion visibility    
            st.radio("Promotion Visibility", ["Public - Anyone can see", "Followers Only", "Private - Invitation Only"], horizontal=True)
            
            # Submit
            col1, col2 = st.columns([3, 2])
            with col2:
                premium_feature = st.checkbox("Boost Promotion (Premium Feature)")
            
            st.form_submit_button("Create Promotion", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Active promotions
        st.markdown("### Active Promotions")
        
        # Sample promotions for display
        promotions = [
            {
                "name": "Summer Special",
                "offer": "20% off all items",
                "description": "Special discount for the summer season. Applicable to all menu items.",
                "start_date": "2023-06-01",
                "end_date": "2023-08-31",
                "claims": 12,
                "status": "active"
            },
            {
                "name": "Photo Contest",
                "offer": "Win a free camera",
                "description": "Post your photos with our products for a chance to win a professional camera.",
                "start_date": "2023-06-15",
                "end_date": "2023-07-15",
                "claims": 5,
                "status": "active"
            },
            {
                "name": "Loyalty Reward",
                "offer": "Free dessert",
                "description": "Customers who have visited 5 times get a free dessert with their next purchase.",
                "start_date": "2023-05-01",
                "end_date": "2023-12-31",
                "claims": 28,
                "status": "active"
            }
        ]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(render_promotion_card(promotions[0], card_class="animate-fade-in animate-delay-100"), unsafe_allow_html=True)
            col1a, col1b = st.columns(2)
            with col1a:
                st.button("Edit", key="edit_promo_1", use_container_width=True)
            with col1b:
                st.button("Pause", key="pause_promo_1", use_container_width=True)
        
        with col2:
            st.markdown(render_promotion_card(promotions[1], card_class="animate-fade-in animate-delay-200"), unsafe_allow_html=True)
            col2a, col2b = st.columns(2)
            with col2a:
                st.button("Edit", key="edit_promo_2", use_container_width=True)
            with col2b:
                st.button("Pause", key="pause_promo_2", use_container_width=True)
        
        with col3:
            st.markdown(render_promotion_card(promotions[2], card_class="animate-fade-in animate-delay-300"), unsafe_allow_html=True)
            col3a, col3b = st.columns(2)
            with col3a:
                st.button("Edit", key="edit_promo_3", use_container_width=True)
            with col3b:
                st.button("Pause", key="pause_promo_3", use_container_width=True)
        
        # Promotion performance summary
        st.markdown("### Promotion Performance")
        
        st.markdown("""
        <div class="card card-glass animate-fade-in">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <h3 class="card-title" style="margin: 0;">Overview</h3>
                <div style="display: flex; gap: 10px;">
                    <div style="background: var(--color-neutral-100); color: var(--color-neutral-700); padding: 6px 12px; border-radius: var(--radius-full); font-size: 0.875rem;">Last 30 Days</div>
                    <div style="background: var(--color-primary-100); color: var(--color-primary-700); padding: 6px 12px; border-radius: var(--radius-full); font-size: 0.875rem;">All Time</div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 24px;">
                <div class="stat-card" style="padding: 16px; margin: 0;">
                    <div class="stat-content">
                        <div class="stat-value">45</div>
                        <div class="stat-label">Promotions Created</div>
                    </div>
                </div>
                
                <div class="stat-card" style="padding: 16px; margin: 0;">
                    <div class="stat-content">
                        <div class="stat-value">287</div>
                        <div class="stat-label">Total Claims</div>
                    </div>
                </div>
                
                <div class="stat-card" style="padding: 16px; margin: 0;">
                    <div class="stat-content">
                        <div class="stat-value">62%</div>
                        <div class="stat-label">Conversion Rate</div>
                        <div class="stat-change-positive">↑ 5%</div>
                    </div>
                </div>
                
                <div class="stat-card" style="padding: 16px; margin: 0;">
                    <div class="stat-content">
                        <div class="stat-value">15.3K</div>
                        <div class="stat-label">Promotion Views</div>
                        <div class="stat-change-positive">↑ 12%</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-weight: 600;">Top Performing Promotions</div>
                    <div style="color: var(--color-primary-500); font-size: 0.875rem; cursor: pointer;">View Report</div>
                </div>
                
                <div style="background: var(--color-neutral-50); border-radius: var(--radius-lg); padding: 16px;">
                    <div style="display: grid; grid-template-columns: 3fr 1fr 1fr 1fr; gap: 10px; font-weight: 600; padding-bottom: 10px; border-bottom: 1px solid var(--color-neutral-200); margin-bottom: 10px;">
                        <div>Promotion</div>
                        <div>Claims</div>
                        <div>Conversion</div>
                        <div>Status</div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 3fr 1fr 1fr 1fr; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--color-neutral-100);">
                        <div>Loyalty Reward</div>
                        <div>28</div>
                        <div>78%</div>
                        <div><span style="color: var(--color-success-500);">●</span> Active</div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 3fr 1fr 1fr 1fr; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--color-neutral-100);">
                        <div>Summer Special</div>
                        <div>12</div>
                        <div>65%</div>
                        <div><span style="color: var(--color-success-500);">●</span> Active</div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 3fr 1fr 1fr 1fr; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--color-neutral-100);">
                        <div>Photo Contest</div>
                        <div>5</div>
                        <div>45%</div>
                        <div><span style="color: var(--color-success-500);">●</span> Active</div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 3fr 1fr 1fr 1fr; gap: 10px; padding: 10px 0;">
                        <div>Spring Offer</div>
                        <div>42</div>
                        <div>82%</div>
                        <div><span style="color: var(--color-neutral-400);">●</span> Ended</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Business Analytics")
        
        # Date range selector
        col1, col2 = st.columns([3, 1])
        with col2:
            date_range = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Year to Date", "All Time"])
        
        # Performance overview
        st.markdown("#### Performance Overview")
        
        # Metrics overview with eye-catching design
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stat-card animate-fade-in" style="background: var(--gradient-blue); color: white;">
                <div class="stat-icon" style="background: rgba(255,255,255,0.2); color: white;">👁️</div>
                <div class="stat-content">
                    <div class="stat-value" style="color: white;">5.2K</div>
                    <div class="stat-label" style="color: rgba(255,255,255,0.9);">Profile Views</div>
                    <div style="display: flex; align-items: center; gap: 4px; color: rgba(255,255,255,0.9); font-size: 0.8rem;">
                        <span>↑ 12%</span>
                        <span style="font-size: 0.75rem;">vs. previous period</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card animate-fade-in animate-delay-100" style="background: var(--gradient-purple); color: white;">
                <div class="stat-icon" style="background: rgba(255,255,255,0.2); color: white;">👥</div>
                <div class="stat-content">
                    <div class="stat-value" style="color: white;">245</div>
                    <div class="stat-label" style="color: rgba(255,255,255,0.9);">Followers</div>
                    <div style="display: flex; align-items: center; gap: 4px; color: rgba(255,255,255,0.9); font-size: 0.8rem;">
                        <span>↑ 8%</span>
                        <span style="font-size: 0.75rem;">vs. previous period</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card animate-fade-in animate-delay-200" style="background: var(--gradient-pink); color: white;">
                <div class="stat-icon" style="background: rgba(255,255,255,0.2); color: white;">📸</div>
                <div class="stat-content">
                    <div class="stat-value" style="color: white;">56</div>
                    <div class="stat-label" style="color: rgba(255,255,255,0.9);">Media Mentions</div>
                    <div style="display: flex; align-items: center; gap: 4px; color: rgba(255,255,255,0.9); font-size: 0.8rem;">
                        <span>↑ 23%</span>
                        <span style="font-size: 0.75rem;">vs. previous period</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-card animate-fade-in animate-delay-300" style="background: var(--gradient-success); color: white;">
                <div class="stat-icon" style="background: rgba(255,255,255,0.2); color: white;">🎯</div>
                <div class="stat-content">
                    <div class="stat-value" style="color: white;">82%</div>
                    <div class="stat-label" style="color: rgba(255,255,255,0.9);">Engagement Rate</div>
                    <div style="display: flex; align-items: center; gap: 4px; color: rgba(255,255,255,0.9); font-size: 0.8rem;">
                        <span>↑ 5%</span>
                        <span style="font-size: 0.75rem;">vs. previous period</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Engagement charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Engagement Over Time")
            st.markdown("""
            <div class="chart-container animate-fade-in">
                <div class="chart-content">
                    <!-- Placeholder for chart -->
                    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column; color: var(--color-neutral-400);">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                        <div style="margin-top: 12px; font-size: 0.9rem;">Engagement trend visualization</div>
                        <div style="margin-top: 6px; font-size: 0.8rem;">Views, followers, and interactions</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Audience Demographics")
            st.markdown("""
            <div class="chart-container animate-fade-in">
                <div class="chart-content">
                    <!-- Placeholder for chart -->
                    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column; color: var(--color-neutral-400);">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>
                        <div style="margin-top: 12px; font-size: 0.9rem;">Audience demographics visualization</div>
                        <div style="margin-top: 6px; font-size: 0.8rem;">Age, interests, and location data</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Content performance
        st.markdown("#### Content Performance")
        st.markdown("""
        <div class="card card-glass animate-fade-in">
            <h3 class="card-title">Top Performing Content</h3>
            
            <div style="margin-bottom: 24px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; margin-bottom: 10px; font-weight: 600; padding-bottom: 10px; border-bottom: 1px solid var(--color-neutral-200);">
                    <div>Content</div>
                    <div>Type</div>
                    <div>Engagement</div>
                    <div>Reach</div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--color-neutral-100); align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 40px; height: 40px; border-radius: var(--radius-lg); overflow: hidden;">
                            <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8Zm9vZHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div>Summer Menu Launch</div>
                    </div>
                    <div>Post</div>
                    <div>
                        <div style="font-weight: 600;">94%</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">128 likes, 42 comments</div>
                    </div>
                    <div>
                        <div style="font-weight: 600;">1.2K</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">Views</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--color-neutral-100); align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 40px; height: 40px; border-radius: var(--radius-lg); overflow: hidden;">
                            <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cmVzdGF1cmFudCUyMGludGVyaW9yfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div>Restaurant Tour</div>
                    </div>
                    <div>Photo Album</div>
                    <div>
                        <div style="font-weight: 600;">87%</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">96 likes, 28 comments</div>
                    </div>
                    <div>
                        <div style="font-weight: 600;">845</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">Views</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; padding: 12px 0; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 40px; height: 40px; border-radius: var(--radius-lg); overflow: hidden;">
                            <img src="https://images.unsplash.com/photo-1482049016688-2d3e1b311543?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTB8fGZvb2R8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div>Chef's Special Event</div>
                    </div>
                    <div>Event</div>
                    <div>
                        <div style="font-weight: 600;">82%</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">78 likes, 35 comments</div>
                    </div>
                    <div>
                        <div style="font-weight: 600;">760</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">Views</div>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <button class="welcome-button welcome-button-secondary" style="padding: 8px 16px;">View All Content</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Location insights
        st.markdown("#### Location Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="card card-glass animate-fade-in">
                <h3 class="card-title">Visitor Location Heat Map</h3>
                <div style="height: 300px; background: var(--color-neutral-100); border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; color: var(--color-neutral-500);">
                    <div style="text-align: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                        <div style="margin-top: 12px; font-size: 0.9rem;">Geographic distribution visualization</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card card-glass animate-fade-in">
                <h3 class="card-title">Top Visitor Locations</h3>
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div>New York City</div>
                        <div style="font-weight: 600;">64%</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 64%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div>Brooklyn</div>
                        <div style="font-weight: 600;">18%</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 18%;"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div>Queens</div>
                        <div style="font-weight: 600;">12%</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 12%;"></div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div>Other</div>
                        <div style="font-weight: 600;">6%</div>
                    </div>
                    <div style="background: var(--color-neutral-200); height: 8px; border-radius: var(--radius-full); overflow: hidden;">
                        <div style="background: var(--gradient-blue); height: 100%; width: 6%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Download analytics
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.button("Download Analytics Report", use_container_width=True)
    
    with tab4:
        st.markdown("### Business Settings")
        
        # Business profile settings
        st.markdown("#### Business Profile")
        with st.form("business_profile"):
            col1, col2 = st.columns(2)
            
            with col1:
                business_name = st.text_input("Business Name", value=business_info.get("business_name", ""))
                
                business_category = st.selectbox("Business Category", 
                                              ["Food & Drink", "Retail", "Services", "Entertainment", 
                                               "Health & Wellness", "Education", "Travel", "Other"],
                                              index=["Food & Drink", "Retail", "Services", "Entertainment", 
                                                    "Health & Wellness", "Education", "Travel", "Other"].index(business_info.get("category", "Food & Drink")))
                
                business_phone = st.text_input("Business Phone", value=business_info.get("phone", ""))
                business_email = st.text_input("Business Email", value=business_info.get("email", ""))
                business_website = st.text_input("Website URL", value=business_info.get("website", ""))
            
            with col2:
                business_desc = st.text_area("Business Description", height=123, value=business_info.get("description", ""))
                business_hours = st.text_area("Business Hours", height=123, value=business_info.get("hours", ""))
            
            st.markdown("#### Location")
            col1, col2 = st.columns(2)
            
            with col1:
                business_address = st.text_input("Street Address", value=business_info.get("address", ""))
                business_city = st.text_input("City", value=business_info.get("city", ""))
            
            with col2:
                business_state = st.text_input("State/Province", value=business_info.get("state", ""))
                business_zip = st.text_input("ZIP/Postal Code", value=business_info.get("zip", ""))
            
            st.markdown("#### Social Media")
            col1, col2 = st.columns(2)
            
            with col1:
                business_instagram = st.text_input("Instagram", value=business_info.get("instagram", ""), placeholder="@yourbusiness")
                business_facebook = st.text_input("Facebook", value=business_info.get("facebook", ""), placeholder="facebook.com/yourbusiness")
            
            with col2:
                business_twitter = st.text_input("Twitter", value=business_info.get("twitter", ""), placeholder="@yourbusiness")
                business_yelp = st.text_input("Yelp", value=business_info.get("yelp", ""), placeholder="yelp.com/biz/yourbusiness")
            
            st.markdown("#### Profile Media")
            col1, col2 = st.columns(2)
            
            with col1:
                st.file_uploader("Business Logo", type=["jpg", "jpeg", "png"])
            
            with col2:
                st.file_uploader("Cover Image", type=["jpg", "jpeg", "png"])
            
            gallery_images = st.file_uploader("Gallery Images (up to 10)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            
            # Submit buttons
            col1, col2 = st.columns(2)
            with col1:
                st.form_submit_button("Save Changes", use_container_width=True)
            with col2:
                st.form_submit_button("Cancel", use_container_width=True)
        
        # Business verification
        st.markdown("#### Business Verification")
        
        if not business_info.get("verified", False):
            st.markdown("""
            <div class="card card-glass animate-fade-in">
                <div style="display: flex; gap: 24px; align-items: center;">
                    <div style="font-size: 3rem;">🔒</div>
                    <div style="flex-grow: 1;">
                        <h3 style="margin-bottom: 8px;">Verify Your Business</h3>
                        <p style="margin-bottom: 16px;">Verified businesses receive a badge that builds trust with customers and unlocks premium features.</p>
                        <button class="welcome-button welcome-button-primary">Start Verification Process</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card card-glass animate-fade-in" style="background: var(--color-success-50); border: 1px solid var(--color-success-200);">
                <div style="display: flex; gap: 24px; align-items: center;">
                    <div style="font-size: 3rem;">✓</div>
                    <div style="flex-grow: 1;">
                        <h3 style="margin-bottom: 8px; color: var(--color-success-700);">Business Verified</h3>
                        <p style="margin-bottom: 0; color: var(--color-success-600);">Your business is verified and eligible for all premium features.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Payment settings
        st.markdown("#### Payment Settings")
        
        # Subscription plan
        st.markdown("""
        <div class="card card-glass animate-fade-in">
            <h3 class="card-title">Subscription Plan</h3>
            
            <div style="background: var(--color-primary-50); border: 1px solid var(--color-primary-200); border-radius: var(--radius-lg); padding: 24px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>
                        <div style="font-weight: 700; font-size: 1.25rem; color: var(--color-primary-700);">Business Pro</div>
                        <div style="color: var(--color-primary-600);">Your current plan</div>
                    </div>
                    <div style="background: var(--color-primary-100); color: var(--color-primary-700); padding: 6px 12px; border-radius: var(--radius-full); font-size: 0.875rem; font-weight: 600;">Active</div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <div style="font-size: 2rem; font-weight: 700; color: var(--color-primary-700);">$29.99<span style="font-size: 1rem; font-weight: 500; color: var(--color-primary-600);">/month</span></div>
                    <div style="color: var(--color-primary-600); font-size: 0.875rem;">Billed monthly • Renews on July 15, 2023</div>
                </div>
                
                <div style="color: var(--color-primary-700);">
                    <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Unlimited promotions
                    </div>
                    <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Advanced analytics
                    </div>
                    <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Priority support
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Promoted visibility
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 12px;">
                <button class="welcome-button welcome-button-secondary" style="flex: 1;">Change Plan</button>
                <button class="welcome-button welcome-button-secondary" style="flex: 1;">Billing History</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment methods
        st.markdown("""
        <div class="card card-glass animate-fade-in">
            <h3 class="card-title">Payment Methods</h3>
            
            <div style="border: 1px solid var(--color-neutral-200); border-radius: var(--radius-lg); padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 40px; height: 30px; background: var(--color-neutral-100); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; color: var(--color-neutral-800);">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
                        </div>
                        <div>
                            <div style="font-weight: 600;">Visa ending in 4242</div>
                            <div style="font-size: 0.8rem; color: var(--color-neutral-500);">Expires 05/2025</div>
                        </div>
                    </div>
                    <div style="background: var(--color-success-100); color: var(--color-success-700); padding: 4px 8px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600;">Default</div>
                </div>
            </div>
            
            <button class="welcome-button welcome-button-secondary">Add Payment Method</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Legal and compliance
        st.markdown("#### Legal & Compliance")
        
        st.markdown("""
        <div class="card card-glass animate-fade-in">
            <h3 class="card-title">Business Documents</h3>
            
            <div style="margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <div style="font-weight: 600;">Terms of Service</div>
                    <div style="display: flex; gap: 8px;">
                        <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">Edit</button>
                        <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">View</button>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <div style="font-weight: 600;">Privacy Policy</div>
                    <div style="display: flex; gap: 8px;">
                        <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">Edit</button>
                        <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">View</button>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between;">
                    <div style="font-weight: 600;">Refund Policy</div>
                    <div style="display: flex; gap: 8px;">
                        <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">Edit</button>
                        <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">View</button>
                    </div>
                </div>
            </div>
            
            <div style="border-top: 1px solid var(--color-neutral-200); padding-top: 24px;">
                <div style="margin-bottom: 16px; font-weight: 600;">Business Documentation</div>
                
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; background: var(--color-neutral-100); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; color: var(--color-neutral-800);">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600;">Business License</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">Uploaded on May 10, 2023</div>
                    </div>
                    <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">View</button>
                </div>
                
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; background: var(--color-neutral-100); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; color: var(--color-neutral-800);">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600;">Tax ID</div>
                        <div style="font-size: 0.8rem; color: var(--color-neutral-500);">Uploaded on May 10, 2023</div>
                    </div>
                    <button class="welcome-button welcome-button-secondary" style="padding: 4px 8px; font-size: 0.8rem;">View</button>
                </div>
                
                <button class="welcome-button welcome-button-secondary">Upload New Document</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

def settings_page():
    st.markdown("""
    <div class="animate-fade-in" style="margin-bottom: 24px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 8px;">Settings</h1>
        <p style="color: var(--color-neutral-600); font-size: 1.1rem; margin-bottom: 24px;">Customize your Atmosphere experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Profile", "Notifications", "Privacy", "Help & Support"])
    
    with tab1:
        st.markdown("### Profile Settings")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Avatar display
            avatar_data = create_user_avatar(st.session_state["user"].get("full_name", "User"))
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{avatar_data}" style="width: 150px; height: 150px; border-radius: 50%; margin-bottom: 16px; border: 4px solid white; box-shadow: var(--shadow-lg);">
                <button class="welcome-button welcome-button-secondary" style="width: 100%;">Change Photo</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Profile form
            with st.form("profile_form"):
                full_name = st.text_input("Full Name", value=st.session_state["user"].get("full_name", ""))

                # Username (disabled - cannot be changed)
                username = st.text_input("Username", value="@" + st.session_state["user"].get("email", "").split("@")[0] if st.session_state["user"].get("email", "") else "", disabled=True)
                
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
            
