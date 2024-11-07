import React, { useState } from 'react';

interface MonitoringFormProps {
  onFetchOldKeys: (n_hours: number) => void;
  onFetchUnusedKeys: (days_unused: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const MonitoringForm: React.FC<MonitoringFormProps> = ({
  onFetchOldKeys,
  onFetchUnusedKeys,
  setLoading,
  setError,
}) => {
  const [nHours, setNHours] = useState(24);
  const [daysUnused, setDaysUnused] = useState(5);

  const handleFetchOldKeys = () => {
    onFetchOldKeys(nHours);
  };

  const handleFetchUnusedKeys = () => {
    onFetchUnusedKeys(daysUnused);
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <label className="block text-sm font-medium text-gray-700">Access Key 생성 N시간 초과 IAM</label>
          <input
            type="number"
            value={nHours}
            onChange={(e) => setNHours(Number(e.target.value))}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2"
          />
          <button
            onClick={handleFetchOldKeys}
            className="mt-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors"
          >
            오래된 키 사용자 조회
          </button>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <label className="block text-sm font-medium text-gray-700">Access Key 미사용 N일 초과 IAM</label>
          <input
            type="number"
            value={daysUnused}
            onChange={(e) => setDaysUnused(Number(e.target.value))}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2"
          />
          <button
            onClick={handleFetchUnusedKeys}
            className="mt-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded transition-colors"
          >
            미사용 키 사용자 조회
          </button>
        </div>
      </div>
    </div>
  );
};