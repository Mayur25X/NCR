import java.util.Scanner;
import java.util.HashSet;
import java.util.*;
class Main {
    public static void swap(char arr[], int i, int j) {
        char temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public static int get_special_strings_count(String str, String beauty) {
        HashSet<String> hs = new HashSet<String>();
        hs.add("" + beauty.charAt(0) + beauty.charAt(0));
        hs.add("" + beauty.charAt(0) + beauty.charAt(1));
        hs.add("" + beauty.charAt(1) + beauty.charAt(0));
        hs.add("" + beauty.charAt(1) + beauty.charAt(1));
        HashSet<String> beauty_strings = new HashSet<String>();
        findBeautiful(0, str.toCharArray(), hs, beauty_strings);
        if (beauty_strings.size() == 0)
            return -1;
        return beauty_strings.size();
    }

    public static void findBeautiful(int start, char arr[], HashSet<String> hs, HashSet<String> beauty_strings) {
        if (start == arr.length) {
            if (beautiful(arr, hs))
                beauty_strings.add(new String(arr));
            return;
        }
        for (int index = start; index < arr.length; index++) {
            swap(arr, start, index);
            findBeautiful(start + 1, arr, hs, beauty_strings);
            swap(arr, start, index);
        }
    }

    public static boolean beautiful(char arr[], HashSet<String> hs) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (hs.contains("" + arr[i] + arr[i + 1])) {
                return false;
            }
        }
        return true;
    }

    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        int n = Integer.parseInt(sc.nextLine());
        int[] res = new int[n];
        for (int i = 0; i < n; i++) {
            String str = sc.nextLine();
            String beauty = sc.nextLine();
            res[i] = get_special_strings_count(str, beauty);
        }
        for (int i = 0; i < n; i++)
            System.out.println(res[i]);

        sc.close();
    }
}
