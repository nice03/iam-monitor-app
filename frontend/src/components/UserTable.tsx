// src/components/UserTable.tsx
import React from 'react';
import { IAMUser } from '../types';

interface UserTableProps {
  users: IAMUser[];
  loading: boolean;
}

export const UserTable: React.FC<UserTableProps> = ({ users, loading }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center p-4">
        <div>로딩 중...</div>
      </div>
    );
  }

  return (
    <table className="min-w-full bg-white shadow-md rounded-lg">
      <thead className="bg-gray-50">
        <tr>
          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            사용자 이름
          </th>
          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            키 생성 후 경과시간
          </th>
          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            키 생성일
          </th>
          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            마지막 사용일
          </th>
          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            액세스 키 상태
          </th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-200">
        {users.map((user) => (
          <tr key={`${user.UserId}-${user.access_keys[0].key_id}`} className="hover:bg-gray-50">
            <td className="px-4 py-3 whitespace-nowrap">
              <div className="text-sm font-medium text-gray-900">{user.UserName}</div>
            </td>
            <td className="px-4 py-3 whitespace-nowrap">
              <div className="text-sm text-gray-500">{user.AccessKeyAge}</div>
            </td>
            <td className="px-4 py-3 whitespace-nowrap">
              <div className="text-sm text-gray-500">{user.AccessKeyCreateDate}</div>
            </td>
            <td className="px-4 py-3 whitespace-nowrap">
              <div className="text-sm text-gray-500">{user.LastUsedDate}</div>
            </td>
            <td className="px-4 py-3 whitespace-nowrap">
  {user.access_keys.map((key) => (
    <div key={key.key_id} className="flex items-center space-x-2 mb-1">
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          key.status === 'Active' 
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}
      >
        {key.status}
      </span>
      <span className="text-sm text-gray-600">{key.key_id}</span>
    </div>
  ))}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};