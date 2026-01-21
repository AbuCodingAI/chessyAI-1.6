"""
Overfitting Detection Module
Monitors training and validation loss to detect and prevent overfitting
"""

class OverfittingDetector:
    """
    Detects overfitting by monitoring the gap between training and validation loss.
    Automatically stops training when overfitting is detected.
    """
    
    def __init__(self, patience=5, min_delta=0.001, verbose=True):
        """
        Initialize the overfitting detector.
        
        Args:
            patience: Number of epochs to wait before stopping (default: 5)
            min_delta: Minimum improvement threshold (default: 0.001)
            verbose: Print debug messages (default: True)
        """
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        
        self.best_val_loss = float('inf')
        self.overfitting_counter = 0
        self.best_model_weights = None
        self.best_epoch = 0
        
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'is_overfitting': [],
            'epoch': []
        }
    
    def check(self, epoch, train_loss, val_loss, model=None):
        """
        Check for overfitting.
        
        Args:
            epoch: Current epoch number
            train_loss: Training loss for this epoch
            val_loss: Validation loss for this epoch
            model: Model object (optional, for saving weights)
            
        Returns:
            Tuple of (is_overfitting, should_stop)
        """
        is_overfitting = False
        should_stop = False
        
        # Record history
        self.history['epoch'].append(epoch)
        self.history['train_loss'].append(train_loss)
        self.history['val_loss'].append(val_loss)
        
        # Check if validation loss improved
        if val_loss < self.best_val_loss - self.min_delta:
            # Validation loss improved
            self.best_val_loss = val_loss
            self.best_epoch = epoch
            self.overfitting_counter = 0
            
            # Save best model weights
            if model is not None:
                try:
                    self.best_model_weights = model.get_weights()
                except:
                    pass
            
            if self.verbose:
                print(f"✅ Epoch {epoch}: Validation loss improved to {val_loss:.6f}")
        else:
            # Validation loss not improving
            if train_loss < self.best_val_loss * 0.95:
                # But training loss is still decreasing - OVERFITTING!
                is_overfitting = True
                self.overfitting_counter += 1
                
                if self.verbose:
                    print(f"⚠️  Epoch {epoch}: Overfitting detected!")
                    print(f"   Train loss: {train_loss:.6f} (decreasing)")
                    print(f"   Val loss: {val_loss:.6f} (not improving)")
                    print(f"   Overfitting counter: {self.overfitting_counter}/{self.patience}")
            else:
                # Both losses not improving - plateau
                self.overfitting_counter += 1
                
                if self.verbose:
                    print(f"⚠️  Epoch {epoch}: No improvement (plateau)")
                    print(f"   Train loss: {train_loss:.6f}")
                    print(f"   Val loss: {val_loss:.6f}")
                    print(f"   Counter: {self.overfitting_counter}/{self.patience}")
        
        self.history['is_overfitting'].append(is_overfitting)
        
        # Check if we should stop
        if self.overfitting_counter >= self.patience:
            should_stop = True
            
            if self.verbose:
                print(f"\n🛑 Stopping training due to overfitting!")
                print(f"   Best epoch: {self.best_epoch}")
                print(f"   Best validation loss: {self.best_val_loss:.6f}")
                
                if self.best_model_weights is not None:
                    print(f"   Restoring best model weights...")
                    if model is not None:
                        try:
                            model.set_weights(self.best_model_weights)
                            print(f"   ✅ Best model restored!")
                        except:
                            print(f"   ❌ Failed to restore model weights")
        
        return is_overfitting, should_stop
    
    def get_summary(self):
        """Get a summary of the training history."""
        return {
            'best_epoch': self.best_epoch,
            'best_val_loss': self.best_val_loss,
            'total_epochs': len(self.history['epoch']),
            'overfitting_epochs': sum(self.history['is_overfitting']),
            'history': self.history
        }
    
    def plot_history(self, save_path=None):
        """
        Plot training and validation loss history.
        
        Args:
            save_path: Path to save the plot (optional)
        """
        try:
            import matplotlib.pyplot as plt
            
            epochs = self.history['epoch']
            train_losses = self.history['train_loss']
            val_losses = self.history['val_loss']
            
            plt.figure(figsize=(10, 6))
            plt.plot(epochs, train_losses, label='Training Loss', marker='o')
            plt.plot(epochs, val_losses, label='Validation Loss', marker='s')
            plt.axvline(x=self.best_epoch, color='g', linestyle='--', label=f'Best Epoch ({self.best_epoch})')
            
            # Highlight overfitting regions
            for i, is_overfitting in enumerate(self.history['is_overfitting']):
                if is_overfitting:
                    plt.axvspan(epochs[i] - 0.5, epochs[i] + 0.5, alpha=0.2, color='red')
            
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.title('Training vs Validation Loss (Overfitting Detection)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            if save_path:
                plt.savefig(save_path, dpi=100, bbox_inches='tight')
                print(f"📊 Plot saved to {save_path}")
            
            plt.show()
        except ImportError:
            print("⚠️  Matplotlib not installed. Cannot plot history.")


# Example usage
if __name__ == '__main__':
    # Create detector
    detector = OverfittingDetector(patience=5, verbose=True)
    
    # Simulate training
    print("Simulating training with overfitting...\n")
    
    train_losses = [0.5, 0.4, 0.3, 0.25, 0.22, 0.20, 0.19, 0.18, 0.17, 0.16]
    val_losses = [0.5, 0.4, 0.35, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40, 0.41]
    
    for epoch, (train_loss, val_loss) in enumerate(zip(train_losses, val_losses)):
        is_overfitting, should_stop = detector.check(epoch, train_loss, val_loss)
        
        if should_stop:
            print(f"\n✅ Training stopped at epoch {epoch}")
            break
    
    # Print summary
    print("\n" + "="*50)
    print("TRAINING SUMMARY")
    print("="*50)
    summary = detector.get_summary()
    print(f"Best epoch: {summary['best_epoch']}")
    print(f"Best validation loss: {summary['best_val_loss']:.6f}")
    print(f"Total epochs: {summary['total_epochs']}")
    print(f"Overfitting epochs: {summary['overfitting_epochs']}")
