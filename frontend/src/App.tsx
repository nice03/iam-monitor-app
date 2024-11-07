import React, { useState } from 'react';
import { MonitoringForm } from './components/MonitoringForm';
import { UserTable } from './components/UserTable';
import { IAMUser, APIResponse, transformAPIResponse } from './types';
import axios from 'axios';

const API_BASE_PATH = '/api/iam';

const App: React.FC = () => {
  const [users, setUsers] = useState<IAMUser[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUsersWithOldKeys = async (n_hours: number): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<APIResponse>(`${API_BASE_PATH}/users`, { 
        params: { n: n_hours }
      });
      console.log('API Response:', response.data);
      
      const transformedUsers = response.data.users.map(transformAPIResponse);
      console.log('Transformed Users:', transformedUsers);
      
      setUsers(transformedUsers);
    } catch (err) {
      console.error("Error fetching users with old keys:", err);
      setError('Failed to fetch users with old keys');
    } finally {
      setLoading(false);
    }
  };

  const fetchUnusedKeys = async (days_unused: number): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<APIResponse>(`${API_BASE_PATH}/unused-keys`, {
        params: { days: days_unused }
      });
      console.log('API Response:', response.data);
      
      const transformedUsers = response.data.users.map(transformAPIResponse);
      console.log('Transformed Users:', transformedUsers);
      
      setUsers(transformedUsers);
    } catch (err) {
      console.error("Error fetching users with unused keys:", err);
      setError('Failed to fetch users with unused keys');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">IAM User Monitor</h1>
      <MonitoringForm
        onFetchOldKeys={fetchUsersWithOldKeys}
        onFetchUnusedKeys={fetchUnusedKeys}
        setLoading={setLoading}
        setError={setError}
      />
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      <UserTable users={users} loading={loading} />
    </div>
  );
};

export default App;