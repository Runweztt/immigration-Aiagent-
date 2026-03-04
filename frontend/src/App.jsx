import React, { useState } from 'react';
import RegistrationForm from './components/RegistrationForm';
import SuccessPage from './components/SuccessPage';
import Layout from './components/Layout';

function App() {
  const [step, setStep] = useState('register');
  const [userData, setUserData] = useState(null);

  const handleRegistrationSuccess = (data) => {
    setUserData(data);
    setStep('success');
  };

  return (
    <Layout>
      {step === 'register' && (
        <RegistrationForm onSafeSuccess={handleRegistrationSuccess} />
      )}
      {step === 'success' && (
        <SuccessPage userData={userData} />
      )}
    </Layout>
  );
}

export default App;
