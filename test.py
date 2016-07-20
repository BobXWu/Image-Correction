#算法测试，HoughLine  没走通
# coding=utf-8
import cv2
import numpy as np


def drawline(img, rho, theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 200 * (-b))
    y1 = int(y0 + 200 * (a))
    x2 = int(x0 - 200 * (-b))
    y2 = int(y0 - 200 * (a))
    if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    else:
        cv2.line(img, (x1, y1), (x2, y2), (255, 102, 21))


if __name__ == "__main__":
    img = cv2.imread("rotate.jpg", 0)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    threshold = 120
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=threshold)  # 这里对最后一个参数使用了经验型的值
    # while lines is None or len(lines) < 4:
    #     threshold -= 10
    #     lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)

    result = img.copy()
    print lines

    horizonline = []
    verticaline = []


    # for line in lines[0]:
    #     rho = line[0]  # 第一个元素是距离rho
    #     theta = line[1]  # 第二个元素是角度theta
    #     print rho
    #     print theta
    #     if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):  # 垂直直线
    #         # 该直线与第一行的交点
    #         pt1 = (int(rho / np.cos(theta)), 0)
    #         # 该直线与最后一行的焦点
    #         pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])
    #         # 绘制一条白线
    #         cv2.line(result, pt1, pt2, (255))
    #     else:  # 水平直线
    #         # 该直线与第一列的交点
    #         pt1 = (0, int(rho / np.sin(theta)))
    #         # 该直线与最后一列的交点
    #         pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))
    #         # 绘制一条直线
    #         cv2.line(result, pt1, pt2, (0), 1)

    for line in lines[0]:
        rho = line[0]  # 第一个元素是距离rho
        theta = line[1]  # 第二个元素是角度theta
        if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):  # 垂直直线
            verticaline.append([rho, theta])
        else:
            horizonline.append([rho, theta])

    topline = []
    bottomline = []
    leftline = []
    rightline = []

    horizonline = sorted(horizonline, key=lambda x: x[1])
    verticaline = sorted(verticaline, key=lambda x: x[0])
    topline = horizonline[0]
    bottomline = horizonline[len(horizonline) - 1]
    leftline = verticaline[0]
    rightline = verticaline[(len(verticaline) - 1)]

    # for i in range(0, len(horizonline)-1):
    #     rho = horizonline[i][0]
    #     theta = horizonline[i][1]
    #     drawline(result, rho, theta)
    #     print rho, theta
    #     cv2.waitKey(0)

    print "edges:",edges
    print horizonline
    print bottomline
    drawline(result, topline[0], topline[1])
    # drawline(result, bottomline[0],bottomline[1])
    drawline(result, leftline[0], leftline[1])
    drawline(result, rightline[0], rightline[1])



    cv2.imshow('Canny', edges)
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
