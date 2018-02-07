# ctr-criteo
2016.11.29

online_experiments:

0. prepare_dataset.py   将数据转换为csv格式

1. online_lbfgs.py
   结果： /output/online_lbfgs/detail.txt

2. online_data.py

3. vw_default_sgd.py
   结果： /output/vw_default_sgd/detail.txt

4. vw_sgd.py
   结果： /output/vw_sgd/detail.txt

5. vw_pistol.py
   结果： /output/vw_pistol/detail.txt

6. vw_ftrl.py
   结果： /output/vw_ftrl/detail.txt



batch_experients:

全属性：

/data_processing/
0. prepare_dataset.py   将数据转换为csv格式, online_experiments 已做

1. shuffle.py   打乱顺序
   注：这个程序有问题，会产生很大的数据量, 另外这个程序也可以不要，舍去

2. count.py 为gbdt建立频繁表
   结果： /output/fc.trav.t10.txt  出现频率超过10的表

3. k-fold_loop_split.py -> split_worker.py 交叉验证划分 并行运行
   结果：'../output/cross_validation_split/'

4. 交叉验证
    /lbfgs_b12/
    将所有特征当做分类特征处理成vw格式进行训练预测，用拟牛顿法（bfgs）优化
    cross_validation.py -> lbfgs_b12.py -> csv2vw_all_categorical.py
    lbfgs_b12.py -> vw_to_submission
    cross_validation.py ->evaluate.py

    注：可调整l2的参数得出不同的结果以选择最佳参数

5. /vw_default_all_categorical
    特征处理方式同实验4，只是训练参数不一样
    cross_validator.py -> vw_default_all_categorical.py -> csv2vw_all_categorical.py

6. /vw_lbfgs_all_categorical
   特征处理方式同实验4，只是训练参数不一样
   cross_validator.py -> vw_lbfgs_all_categorical.py -> csv2vw_all_categorical.py


特征值预处理： /python/

/vw_default_statical/
数值特征：特征=特征值， 分类特征：特征-特征值=该特征值的点击率（取出现次数超过10次的特征-特征值）
0. cross_validator.py -> vw_default_statical.py -> csv2vw_statical.py
   vw_default_statical.py -> vw_to_submission.py
   cross_validator.py -> evaluate.py
ffm
fm
vw
/vw_lfgs_statical/
1. cross_validator.py -> vw_lfgs_statical.py -> csv2vw_statical.py
   vw_lfgs_statical.py -> vw_to_submission.py
   cross_validator.py -> evaluate.py

对特征进行标准化处理：
数值特征, 大于2的, v = log(v)**2, 变为分类特征，小于2的，转化为特殊值 SP
分类特征, 出现次数少于10次的转化为特殊值，如C1less, C2less
2. /vw_lbfgs_normalized_categorical/
   cross_validator.py -> vw_lbfgs_normalized_categorical.py -> csv2vw_normalized_categorical.py -> add_dummy_label.py
   csv2vw_normalized_categorical.py -> parallelizer_normalization2csv.py -> normalized2csv.py
   vw_lbfgs_normalized_categorical.py -> vw_to_submission.py
   cross_validator.py -> evaluate.py

   注：parallelizer_normalization2csv.py  实现并行运行, 可以不用

pre-a.py 数值属性，若缺失，填充-10，写入*.dense中，分类特征取出现最频繁的26个特征组合，特征-特征值， 将其编码写入×.sparse中
gbdt 生成z增强特征，写入×.gbdt.out
gbdt2csv.py 将原始特征和增强特征组合成新的特征， 写入×.addition, 原始特征的处理同标准化， 增强特征加在其后面
然后再将×.addition转化为vw格式，进行训练测试
3. /vw_lbfgs_gbdt
   cross_validator.py -> vw_lbfgs_gbdt.py -> csv2vw_gbdt.py -> add_dummy_label.py
   csv2vw_gbdt.py -> parallelizer-a.py -> pre-a.py
   csv2vw_gbdt.py -> ./gbdt
   csv2vw_gbdt.py -> parallelizer-gbdt.py -> gbdt2csv.py
   vw_lbfgs_gbdt.py -> vw_to_submission.py
   cross_validator.py -> evaluate.py

   注： gbdt预处理

4. /lrxgb
    csv2xgboost_onehotencoding.py 数值特征：'{0}:{1}'.format(k.split('I')[1], v)， 分类特征: 先转化为组合特征，特征-特征值(k-v),
    为组合特征建立编号， 然后输出'{0}:1'.format(table.get('k-v')), 模型参数'booster': 'objective': 'binary:logistic',
    'booster':'gblinear'
   cross_validator.py -> LRXGB.py -> csv2xgboost_onehotencoding.py

5. /xgboost_gbdt_onehotencoding
   booster:gbtree
   cross_validator.py -> xgboost_gbdt_onehotencoding.py -> csv2xgboost_onehotencoding.py

6. /xgboost_gbdt
   特征处理方式为统计特征, booster:gbtree
   cross_validator.py -> xgboost_gbdt.py -> csv2xgboost_statistical.py

7. /ffm_normalized
   特征处理方式为标准化，同实验2， ffm训练并预测，输出文件 te.ffm.out
   cross_validator.py -> ffm_normalized.py -> add_dummy_label.py, parallelizer-normalization2ffm.py
   parallelizer-normalization2ffm.py -> normalized2ffm.py

8. /ffm_gbdt
   特征处理方式gbdt，同实验3，只是不用转化为vw格式，将gbdt特征直接用于ffm训练预测，
   cross_validator.py -> ffm_gbdt.py -> add_dummy_label.py, parallelizer-a.py -> pre-a.py, parallelizer-b -> pre-b.py

9. /simple_sgd
   logistic 用sgd优化
   cross_validator.py -> simple_sgd.py

10. /vw_quadratic_features
    csv2vw_quadratic.py 将数值特征的命名空间映射到a-m上，特征值不变，组合为'|{namespace}={v}'，
    将分类特征的命名空间映射到A-Z上,特征值不变，组合为'|{namespace}={v}'
    cross_validator.py -> vw_quadratic_features.py -> csv2vw_quadratic.py

11. /libfm
    数值特征：'{0}:{1}'.format(k.split('I')[1], v)， 分类特征: 先转化为组合特征，特征-特征值(k-v),
    为组合特征建立编号， 然后输出'{0}:1'
    libFM 训练并预测
    cross_validator.py -> libfm.py -> csv2libfm.py


结果分析：
/result_analysis/result_analysis.py

