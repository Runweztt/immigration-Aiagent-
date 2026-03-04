import React, { useState } from 'react';
import RegistrationForm from './components/RegistrationForm';
import SuccessPage from './components/SuccessPage';
import Dashboard from './components/Dashboard';
import Layout from './components/Layout';

function App() {
  const [step, setStep] = useState('register');
  const [userData, setUserData] = useState(null);

  const handleRegistrationSuccess = (data) => {
    setUserData(data);
    setStep('success');
  };

  const handleProceedToDashboard = () => {
    setStep('dashboard');
  };

  return (
    <Layout isFullWidth={step === 'dashboard'}>
      {step === 'register' && (
        <RegistrationForm onSafeSuccess={handleRegistrationSuccess} />
      )}
      {step === 'success' && (
        <SuccessPage userData={userData} onProceed={handleProceedToDashboard} />
      )}
      {step === 'dashboard' && (
        <Dashboard userData={userData} />
      )}
    </Layout>
  );
}

export default App;
