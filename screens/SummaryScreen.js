import React, { useEffect, useState } from 'react';
import {
  View, Text, StyleSheet, FlatList, TouchableOpacity,
  Modal, ScrollView, Dimensions
} from 'react-native';
import axios from 'axios';
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import { SafeAreaView } from 'react-native-safe-area-context';


const screenWidth = Dimensions.get('window').width;
const BACKEND_IP = 'http://172.17.80.103:5000';  
// const BACKEND_IP = 'http://100.65.217.86:5000';
const chartConfig = {
  backgroundGradientFrom: "#e8f5e9",
  backgroundGradientTo: "#c8e6c9",
  decimalPlaces: 1,
  color: (opacity = 1) => `rgba(56, 142, 60, ${opacity})`, 
  labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`, 
  propsForDots: {
    r: "5",
    strokeWidth: "2",
    stroke: "#388e3c"
  },
  propsForLabels: {
    fontSize: 10,
    fontWeight: "bold"
  },
  barPercentage: 0.6
};


const sleepTrendColors = {
  Good: '#4CAF50',
  Moderate: '#FFC107',
  Poor: '#F44336'
};




const SummaryScreen = () => {
  const [summaries, setSummaries] = useState([]);
  const [selectedSummary, setSelectedSummary] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const response = await axios.get(`${BACKEND_IP}/all_summaries`);
      const raw = response.data;
      const sorted = Object.entries(raw).sort((a, b) =>
        new Date(a[1].start_time) < new Date(b[1].start_time) ? 1 : -1
      );
      const formatted = sorted.map(([id, data]) => ({ id, ...data }));
      
      setSummaries(formatted);
    } catch (error) {
      console.error('Failed to fetch summaries:', error.message);
    }
  };

  const renderAnalysis = () => {
    if (!summaries.length) {
      return (
        <View style={{ padding: 20 }}>
          <Text style={{ fontSize: 16, color: '#888' }}>No session summaries found yet.</Text>
        </View>
      );
    }    

    const labels = summaries.map((s) => s.start_time.split(' ')[0]);
    const snoringMins = summaries.map((s) => s.snoring_minutes);
    const totalMins = summaries.map((s) => s.total_sleep_minutes);
    const avgProbs = summaries.map((s) => s.avg_snoring_probability);

    const qualityCounts = summaries.reduce((acc, s) => {
      acc[s.sleep_quality] = (acc[s.sleep_quality] || 0) + 1;
      return acc;
    }, {});

    const pieData = Object.entries(qualityCounts).map(([quality, count]) => ({
      name: quality,
      population: count,
      color: sleepTrendColors[quality],
      legendFontColor: '#333',
      legendFontSize: 10
    }));

    return (
      <View style={styles.analysisContainer}>
        <Text style={styles.header}>📊 Weekly Sleep Trends</Text>
    
        <ScrollView
          horizontal
          pagingEnabled
          showsHorizontalScrollIndicator={false}
        >
          {/* Bar Chart */}
          <View style={styles.chartContainer}>
            <BarChart
              data={{
                labels: labels.map((l, i) => (i % 2 === 0 ? l : '')),
                datasets: [
                  { data: snoringMins, color: () => '#F44336' },
                  { data: totalMins, color: () => '#4CAF50' }
                ]
              }}
              width={screenWidth - 20}
              height={280}
              fromZero
              chartConfig={chartConfig}
              verticalLabelRotation={30}
            />
            <Text style={styles.chartDescription}>
              📉 Bar chart showing total sleep vs. snoring minutes per session.
            </Text>
          </View>
    
          {/* Line Chart */}
          <View style={styles.chartContainer}>
            <LineChart
              data={{
                labels: labels.map((l, i) => (i % 2 === 0 ? l : '')),
                datasets: [{ data: avgProbs }]
              }}
              width={screenWidth - 30}
              height={280}
              chartConfig={chartConfig}
              bezier
            />
            <Text style={styles.chartDescription}>
              📈 Line chart showing average snoring probability per session.
            </Text>
          </View>
    
          {/* Pie Chart */}
          <View style={styles.chartContainer}>
            <PieChart
              data={pieData}
              width={screenWidth - 20}
              height={260}
              chartConfig={chartConfig}
              accessor="population"
              backgroundColor="transparent"
              paddingLeft="15"
              absolute
            />
            <Text style={styles.chartDescription}>
              🧩 Pie chart showing sleep quality distribution (Good, Moderate, Poor).
            </Text>
          </View>
        </ScrollView>
      </View>
    );
    
    
  }

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.itemContainer}
      onPress={() => {
        setSelectedSummary(item);
        setModalVisible(true);
      }}
    >
      <Text style={styles.dateText}>{item.start_time.split(' ')[0]}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      {/* Session List */}
      <Text style={styles.SessionHeader}>Session Reports</Text>
      <View style={{ flex: 0.3 }}>
        <FlatList
          data={summaries}
          renderItem={renderItem}
          keyExtractor={(item) => item.id}
        />
      </View>

      {/* Session Details Popup */}
      <Modal visible={modalVisible} animationType="slide" transparent>
        <View style={styles.modalBackground}>
          <View style={styles.modalContainer}>
            {selectedSummary && (
              <>
                <Text style={styles.modalTitle}>Session Summary</Text>
                <Text>🕐 Start: {selectedSummary.start_time}</Text>
                <Text>🕐 End: {selectedSummary.end_time}</Text>
                <Text>🛌 Total: {selectedSummary.total_sleep_minutes} min</Text>
                <Text>😴 Snoring: {selectedSummary.snoring_minutes} min</Text>
                <Text>📈 Avg Prob: {selectedSummary.avg_snoring_probability}</Text>
                <Text>📋 Quality: {selectedSummary.sleep_quality}</Text>
                <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
                  <Text style={styles.closeText}>Close</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        </View>
      </Modal>

      {/* Weekly Analysis */}
      <View style={{ flex: 0.7 }}>{renderAnalysis()}</View>
      </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 10 },
  itemContainer: {
    padding: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    marginBottom: 8
  },
  dateText: { fontSize: 16, fontWeight: 'bold', color: '#2e7d32' },
  modalBackground: { flex: 1, backgroundColor: 'rgba(0,0,0,0.4)', justifyContent: 'center', alignItems: 'center' },
  modalContainer: { backgroundColor: '#fff', padding: 20, borderRadius: 10, width: '80%' },
  modalTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  closeButton: { marginTop: 20, alignSelf: 'center' },
  closeText: { color: '#2e7d32', fontWeight: 'bold' },
  header: { fontSize: 18, fontWeight: 'bold', marginBottom: 10, color: '#2e7d32' },
  SessionHeader: { fontSize: 22,  fontWeight: 'bold', marginBottom: 10, color: '#2e7d32' },
  analysisContainer: {
    borderRadius: 30,
    marginTop: 100,
    alignItems: 'center',
    justifyContent: 'center',
  },
  chartContainer: {

    borderRadius: 30,
    width: screenWidth - 20,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 10,
  },
  chartDescription: {
    marginTop: 12,
    fontSize: 15,
    color: '#333',
    textAlign: 'center',
    maxWidth: '90%',
    lineHeight: 20,
  },
  
});

export default SummaryScreen;
