import React from 'react';
import { useApp } from './context/AppContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { DashboardView } from './components/views/DashboardView';
import { SkillDAGRoadmap } from './components/views/SkillDAGRoadmap';
import { CareerExplorer } from './components/views/CareerExplorer';
import { JobGapAnalyzer } from './components/views/JobGapAnalyzer';
import { InterviewArena } from './components/views/InterviewArena';
import { ResumeScanner } from './components/views/ResumeScanner';
import { StudyTimer } from './components/views/StudyTimer';
import { ResourcesView } from './components/views/ResourcesView';
import { SkillDetailDrawer } from './components/ui/SkillDetailDrawer';
import { AuthModal } from './components/ui/AuthModal';
import { NotificationDrawer } from './components/ui/NotificationDrawer';
import { AddSkillModal } from './components/ui/AddSkillModal';
import { Toast } from './components/ui/Toast';
import { LoginPage } from './components/ui/LoginPage';
import { AuroraBeam } from './components/effects/AuroraBeam';

export function App() {
  const { activeTab, user, loading, sidebarOpen, setSidebarOpen } = useApp();

  const renderActiveView = () => {
    switch (activeTab) {
      case 'dashboard':    return <DashboardView />;
      case 'roadmap':      return <SkillDAGRoadmap />;
      case 'careers':      return <CareerExplorer />;
      case 'jobs':         return <JobGapAnalyzer />;
      case 'interviews':   return <InterviewArena />;
      case 'resume':       return <ResumeScanner />;
      case 'study':        return <StudyTimer />;
      case 'resources':    return <ResourcesView />;
      default:             return <DashboardView />;
    }
  };

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#000000',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div className="animate-glow" style={{
            width: '48px',
            height: '48px',
            borderRadius: '14px',
            background: 'linear-gradient(135deg, #059669, #22d3ee)',
            margin: '0 auto 16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <span style={{ fontSize: '1.5rem' }}>⚡</span>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Loading CareerPath AI...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', position: 'relative' }}>
      {/* Aurora Beam Background Effect */}
      <div className="bg-aurora-container">
        <AuroraBeam
          color="#34d399"
          midColor="#22d3ee"
          deepColor="#a78bfa"
          speed={0.8}
          sheets={5}
          amplitude={0.12}
          frequency={3.2}
          thickness={0.05}
          tail={0.22}
          position={0.0}
          slant={0.1}
          spread={0.16}
          rays={0.45}
          rayScale={26}
          rayDrift={0.8}
          reactivity={0.7}
          gain={1.5}
          exposure={2.4}
          contrast={1.0}
          hueDrift={1.0}
          grain={0.05}
          opacity={0.85}
          cursorInteraction={true}
          cursorSway={0.5}
          backgroundColor="transparent"
        />
      </div>

      {/* Background ambient lighting */}
      <div className="bg-mesh" />
      <div className="bg-grid" />

      {/* Top Navigation */}
      <Navbar />

      {/* Main Layout Body */}
      <div style={{ display: 'flex', flex: 1, position: 'relative', zIndex: 1 }}>
        <div
          className={`app-drawer-backdrop${sidebarOpen ? ' is-open' : ''}`}
          onClick={() => setSidebarOpen(false)}
        />
        <Sidebar />
        <main
          className="animate-fade-in app-main"
          key={activeTab}
          style={{ flex: 1, padding: '28px 36px', overflowY: 'auto', maxHeight: 'calc(100vh - 68px)' }}
        >
          {renderActiveView()}
        </main>
      </div>

      {/* Floating Drawers & Modals */}
      <SkillDetailDrawer />
      <AuthModal />
      <NotificationDrawer />
      <AddSkillModal />
      <Toast />
    </div>
  );
}

export default App;
