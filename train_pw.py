import nn.my_model as my_model
import nn.loss as L
import nn.datagen as dg
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import CSVLogger, ModelCheckpoint


class base:
    def __init__(self):
        self.input_shape = [112, 112, 3]
        self.model = my_model.create_model(self.input_shape)
        self.batch = 2
        self.step_t = 3200
        self.sample = 64
        self.epochs = 1000
        self.step_v = int(self.step_t / 32)
        self.learning_rate = 1e-3
        self.optimizer = optimizers.Adam(learning_rate=self.learning_rate)

    def train(self, metric, pretrain=''):
        if (len(pretrain) > 0):
            self.model.load_weights(pretrain)
        self.model.compile(
            loss=L.pairwise_loss(metric),
            optimizer=self.optimizer,
            metrics=[L.pos_neg_all(metric)])

        csv_logger = CSVLogger('log_pw.csv', append=True, separator=';')
        checkpoint = ModelCheckpoint(
            f"./weights/best_{metric}_pw.hdf5",
            monitor='loss', verbose=1,
            save_best_only=True,
            mode='auto', save_freq='epoch')
        callbacks_list = [csv_logger, checkpoint]

        self.model.fit(
            x=dg.ms1m_gen_batch(
                self.batch, self.sample),
            epochs=self.epochs,
            steps_per_epoch=self.step_t,
            callbacks=callbacks_list)

        self.model.save_weights(
            f"./weights/final_{metric}_pw.hdf5")


l2 = base()
l2.train('euclid')
