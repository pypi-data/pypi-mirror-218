import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None
__all__ = ['generate_precision_recall']


class _ConfusionMatrix:
    def __init__(self, num_classes, CONF_THRESHOLD, IOU_THRESHOLD):
        self.matrix = np.zeros((num_classes + 1, num_classes + 1))
        self.num_classes = num_classes
        self.CONF_THRESHOLD = CONF_THRESHOLD
        self.IOU_THRESHOLD = IOU_THRESHOLD

    def box_iou_calc(self, boxes1, boxes2):
        # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
        """
        Return intersection-over-union (Jaccard index) of boxes.
        Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
        Arguments:
            boxes1 (Array[N, 4])
            boxes2 (Array[M, 4])
        Returns:
            iou (Array[N, M]): the NxM matrix containing the pairwise
                IoU values for every element in boxes1 and boxes2
        This implementation is taken from the above link and changed so that it only uses numpy..
        """

        def box_area(box):
            # box = 4xn
            return (box[2] - box[0]) * (box[3] - box[1])
        

        area1 = box_area(boxes1.T)
        area2 = box_area(boxes2.T)

        lt = np.maximum(boxes1[:, None, :2], boxes2[:, :2])  # [N,M,2]
        rb = np.minimum(boxes1[:, None, 2:], boxes2[:, 2:])  # [N,M,2]

        inter = np.prod(np.clip(rb - lt, a_min = 0, a_max = None), 2)
        return inter / (area1[:, None] + area2 - inter)  # iou = inter / (area1 + area2 - inter)
    
    def process_batch(self, detections, labels):
        '''
        Return intersection-over-union (Jaccard index) of boxes.
        Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
        Arguments:
            detections (Array[N, 6]), x1, y1, x2, y2, conf, class
            labels (Array[M, 5]), class, x1, y1, x2, y2
        '''
        conf_detections = []
        for detection in detections:
            if detection[4] >= self.CONF_THRESHOLD:
                conf_detections.append(detection)
        
        detections = np.array(conf_detections)
        labels = np.array(labels)
        if len(labels) != 0:
            gt_classes = labels[:, 0].astype(np.int16)
        else:
            if len(detections):
                detection_classes = detections[:, 5].astype(np.int16)
                for detection_class in detection_classes:
                    self.matrix[self.num_classes, detection_class] += 1
            return
        if len(detections) != 0:
            detection_classes = detections[:, 5].astype(np.int16)
        else:
            if len(labels):
                for gt_class in gt_classes:
                    self.matrix[gt_class, self.num_classes] += 1      
            return

        if len(labels) != 0 and len(detections) != 0:
            all_ious = self.box_iou_calc(labels[:, 1:], detections[:, :4])
            want_idx = np.where(all_ious >= self.IOU_THRESHOLD)
        else:
            all_ious = np.array([[]])
            want_idx = np.array([[]])

        all_matches = []
        for i in range(want_idx[0].shape[0]):
            all_matches.append([want_idx[0][i], want_idx[1][i], all_ious[want_idx[0][i], want_idx[1][i]]])
        
        all_matches = np.array(all_matches)
        if all_matches.shape[0] > 0: # if there is match
            all_matches = all_matches[all_matches[:, 2].argsort()[::-1]]
            all_matches = all_matches[np.unique(all_matches[:, 1], return_index = True)[1]]
            all_matches = all_matches[all_matches[:, 2].argsort()[::-1]]
            all_matches = all_matches[np.unique(all_matches[:, 0], return_index = True)[1]]
        
        for i, label in enumerate(labels):
            if all_matches.shape[0] > 0 and all_matches[all_matches[:, 0] == i].shape[0] == 1:
                gt_class = gt_classes[i]
                detection_class = detection_classes[int(all_matches[all_matches[:, 0] == i, 1][0])]
                self.matrix[(gt_class), detection_class] += 1

            else:
                gt_class = gt_classes[i]
                self.matrix[(gt_class), self.num_classes] += 1
        
        for i, detection in enumerate(detections):
            if all_matches.shape[0] and all_matches[all_matches[:, 1] == i].shape[0] == 0:
                detection_class = detection_classes[i]
                self.matrix[self.num_classes, detection_class] += 1

            elif all_matches.shape[0] == 0:
                detection_class = detection_classes[i]
                self.matrix[self.num_classes, detection_class] += 1

        
    def return_matrix(self):
        return self.matrix

    def print_matrix(self):
        for i in range(self.num_classes + 1):
            print(' '.join(map(str, self.matrix[i])))


def generate_precision_recall(df_gt, df_pred, conf_value=0.5, iou_value=0.5):
    """Return the precision and recall for a given confidence and iou value.

    Args:
        df_gt (pandas dataframe): ground truth dataframe with labels order: "label,frame_id,x0,y0,x1,y1"
        df_pred (pandas dataframe): prediction dataframe with labels order: "x0,y0,x1,y1,confidence,label,frame_id"
        conf_value (float, optional): Confidence value. Defaults to 0.5.
        iou_value (float, optional): IOU threshold value. Defaults to 0.5.

    Returns:
        dict: Dictionary containing list of precision and recall values for each label
    """
    num_frames = df_gt.frame_id.unique().tolist()
    num_frames.extend(df_pred.frame_id.unique().tolist())
    num_frames = list(set(num_frames))
    num_frames.sort()
    labels = df_gt.label.unique().tolist()
    labels.extend(df_pred.label.unique().tolist())
    labels = list(set(labels))
    num_labels = len(labels)
    encoding = [i for i in range(num_labels)]
    cm_obj = _ConfusionMatrix(num_classes=num_labels, CONF_THRESHOLD=conf_value, IOU_THRESHOLD=iou_value)
    for i in num_frames:

        df_gt1 = df_gt[df_gt.frame_id == i]
        df_gt1.drop(columns='frame_id', inplace=True, axis=1)
        df_gt1['label'].replace(labels, encoding, inplace=True)

        df_pred1 = df_pred[df_pred.frame_id == i]
        df_pred1.drop(columns='frame_id', inplace=True, axis=1)
        df_pred1['label'].replace(labels, encoding, inplace=True)

        pred = df_pred1.values.tolist()
        gt = df_gt1.values.tolist()

        cm_obj.process_batch(pred, gt)

    matrix = cm_obj.return_matrix()
    for i in range(num_labels+1):
        for j in range(i+1, num_labels+1):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    labels_copy = labels.copy()
    labels_copy.append('blank')

    precision=[]
    recall = []
    for i in range(num_labels):
        tp = matrix[i][i]
        tp_fp = sum(matrix[i])
        tp_fn = sum([mat[i] for mat in matrix])
        if tp != 0:
            precision.append(tp/tp_fp)
            recall.append(tp/tp_fn)
        else:
            precision.append(0)
            recall.append(0)

    data_plot = {
                'labels': labels,
                'precision': precision, 
                'recall': recall, 
                }

    return data_plot

if __name__ == '__main__':
    df_gt = pd.DataFrame() # dataframe containing columns "label,frame_id,x0,y0,x1,y1"
    df_pred = pd.DataFrame() # dataframe containing columns "x0,y0,x1,y1,confidence,label,frame_id"
    res = generate_precision_recall(df_gt, df_pred, conf_value=0.5, iou_value=0.5)
    print(res)