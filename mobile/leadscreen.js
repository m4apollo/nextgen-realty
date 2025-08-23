// mobile/LeadScreen.js
import React, { useState } from 'react';
import { View, Text, FlatList } from 'react-native';
import { fetchLeads } from '../api';

export default function LeadScreen() {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    const loadLeads = async () => {
      const data = await fetchLeads();
      setLeads(data);
    };
    loadLeads();
  }, []);

  return (
    <View className="p-4">
      <Text className="text-xl font-bold mb-4">Your Leads</Text>
      <FlatList
        data={leads}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <View className="border-b pb-3 mb-3">
            <Text className="font-medium">{item.name}</Text>
            <Text className="text-gray-600">{item.status}</Text>
          </View>
        )}
      />
    </View>
  );
}