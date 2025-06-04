import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from 'react-native';
import Toast from 'react-native-toast-message';
import { Path, Svg } from 'react-native-svg';
import { onValue, ref } from 'firebase/database';
import { database } from '../config/firebaseConfig'; // 
import SessionSummaryModal from '../components/SessionSummary';

const screenWidth = Dimensions.get('window').width;
// const BACKEND_IP = 'http://100.65.217.86:5000';
const BACKEND_IP = 'http://172.17.80.103:5000';

export default function HomeScreen() {
  const [modalVisible, setModalVisible] = useState(false);
  const [sessionData, setSessionData] = useState(null);
  const [waveformData, setWaveformData] = useState([]);
  const [statusColor, setStatusColor] = useState('#4CAF50'); // green

  const MAX_HEIGHT = 100;  // max vertical scale of the waveform

  useEffect(() => {
    const todayKey = new Date().toISOString().split('T')[0]; // 'YYYY-MM-DD'
    const dataRef = ref(database, `users/user123/snoring_data/${todayKey}`);
  
    const unsubscribe = onValue(dataRef, (snapshot) => {
      const data = snapshot.val();
      if (!data) return;
  
      const latestKey = Object.keys(data).sort().pop();
      const latest = data[latestKey];
  
      if (!latest) return;
  
      const { detected_snoring, snoring_prob } = latest;
  
      // 🔴🟡🟢 Color Based on Status
      if (detected_snoring) {
        setStatusColor('#F44336');
      } else if (snoring_prob > 0.3) {
        setStatusColor('#FFC107');
      } else {
        setStatusColor('#4CAF50');
      }
  
      
      const scaledY = (1 - snoring_prob) * MAX_HEIGHT + 20;  
      setWaveformData((prev) => [...prev.slice(-screenWidth + 20), scaledY]);
    });
  
    return () => unsubscribe();
  }, []);
  

  const handleStart = async () => {
    try {
      console.log('[Frontend] Sending /start POST...');
      const res = await fetch(`${BACKEND_IP}/start`, { method: 'POST' });
      const data = await res.json();
      console.log('[Frontend] Response:', data);
  
      if (!res.ok) throw new Error('Failed to start');
  
      Toast.show({ type: 'success', text1: '🛌 Session Started', visibilityTime: 4000 });
    } catch (error) {
      console.log('Start Error:', error);
      Toast.show({ type: 'error', text1: '❌ Failed to Start', text2: error.message, visibilityTime: 4000 });
    }
  };
  

  const handleStop = async () => {
    try {
      const res = await fetch(`${BACKEND_IP}/stop`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to stop');

      const stopData = await res.json();
      Toast.show({ type: 'info', text1: '⏹️ Session Stopped', visibilityTime: 4000 });

      const summaryRes = await fetch(`${BACKEND_IP}/session_summary`);
      const data = await summaryRes.json();
      setSessionData(data);
      setModalVisible(true);
    } catch (error) {
      console.log('Stop Error:', error);
      Toast.show({ type: 'error', text1: '❌ Failed to Stop', visibilityTime: 4000 });
    }
  };

  const renderWavePath = () => {
    if (waveformData.length < 2) return '';
    return waveformData.reduce((path, y, i) => {
      const x = i;
      return path + `${i === 0 ? 'M' : 'L'} ${x} ${y} `;
    }, '');
  };
  

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Snoring Detection</Text>

      <View style={styles.waveContainer}>
        <Svg height="120" width={screenWidth}>
          <Path d={renderWavePath()} fill="none" stroke={statusColor} strokeWidth="3" />
        </Svg>
        <Text style={[styles.statusLabel, { color: statusColor }]}>
          {statusColor === '#4CAF50' ? 'Silent'
            : statusColor === '#FFC107' ? 'Disturbance'
            : 'Snoring'}
        </Text>
      </View>

      <TouchableOpacity style={styles.buttonStart} onPress={handleStart}>
        <Text style={styles.buttonText}>Start Detection</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.buttonStop} onPress={handleStop}>
        <Text style={styles.buttonText}>Stop Detection</Text>
      </TouchableOpacity>

      <SessionSummaryModal
        visible={modalVisible}
        sessionData={sessionData}
        onClose={() => setModalVisible(false)}
      />
      <Toast />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212', alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 26, marginBottom: 10, color: '#fff' },
  waveContainer: {
    height: 140,
    marginBottom: 30,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusLabel: {
    marginTop: -15,
    fontSize: 18,
    fontWeight: 'bold',
  },
  buttonStart: {
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 10,
    marginBottom: 20,
    width: 200,
    alignItems: 'center'
  },
  buttonStop: {
    backgroundColor: '#F44336',
    padding: 15,
    borderRadius: 10,
    width: 200,
    alignItems: 'center'
  },
  buttonText: { color: '#fff', fontSize: 18 },
});
