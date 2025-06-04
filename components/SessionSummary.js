import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Modal } from 'react-native';

const SessionSummaryModal = ({ visible, sessionData, onClose }) => {
  return (
    <Modal visible={visible} transparent={true} animationType="slide">
      <View style={styles.modalContainer}>
        <ScrollView style={styles.modalContent}>
          <Text style={styles.modalTitle}>🛌 Sleep Session Summary</Text>

          {sessionData ? (
            <>
              <Text style={styles.modalText}>Total Sleep: {sessionData.total_sleep_minutes} min</Text>
              <Text style={styles.modalText}>Snoring Time: {sessionData.snoring_minutes} min</Text>
              <Text style={styles.modalText}>Snoring %: {sessionData.snoring_percent}%</Text>
              <Text style={styles.modalText}>Avg Snoring Probability: {sessionData.avg_snoring_probability}</Text>
              <Text style={styles.modalText}>Sleep Quality: {sessionData.sleep_quality}</Text>
            </>
          ) : (
            <Text style={styles.modalText}>Loading...</Text>
          )}

          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <Text style={styles.closeButtonText}>Close</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>
    </Modal>
  );
};

export default SessionSummaryModal;

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 25,
    width: '85%',
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 15,
    textAlign: 'center',
  },
  modalText: {
    fontSize: 16,
    marginVertical: 5,
  },
  closeButton: {
    backgroundColor: '#2196F3',
    padding: 12,
    borderRadius: 8,
    marginTop: 20,
    alignItems: 'center',
  },
  closeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});
